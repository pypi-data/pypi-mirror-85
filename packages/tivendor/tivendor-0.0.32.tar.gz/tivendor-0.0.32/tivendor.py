# python3

import datetime
import time
import json
import logging
from _thread import start_new_thread
from urllib.parse import urlparse

import requests
import redis
from kafka import KafkaProducer

from tisdk.sm4 import encrypt_ecb, decrypt_ecb


try:
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNull'
except Exception as e:
    print(e)


class TiVendorError(Exception):
    pass


class EasyCache:

    # data = {}

    def __init__(self):
        self.data = {}

    def set(self, key, value, ttl=300):
        ts = time.time() + ttl
        self.data[key] = (value, ts)

    def get(self, key, default=None):
        if key not in self.data:
            return default

        value, ts = self.data[key]
        if time.time() > ts:
            self.clear(key)
            return default

        return value

    def clear(self, key):
        if key not in self.data:
            return
        del self.data[key]

    def clear_all(self):
        self.data = {}


class TiVendor:
    cache = EasyCache()
    kafka_producers = {}
    redis_pools = {}
    queue = []

    def __init__(self, config):
        self.tiadmin_host = config['TIADMIN_HOST'] or 'http://tiadmin.kong:8000'
        self.kafka_enable = config.get('KAFKA_ENABLE', 'on')
        self.kafka_host = config.get('KAFKA_HOST') or 'kafka-kafka.kafka:9092'
        self.kafka_topic = config.get('KAFKA_TOPIC') or 'supplier-request'
        self.default_service_name = config.get('DEFAULT_SERVICE_NAME', '')
        self.logger_name = config.get('LOGGER_NAME') or '__main__'

        self.logger = logging.getLogger(self.logger_name)
        self.kafka_producer = self.get_singleton_kafka_producer()

        self.redis_host = config.get('REDIS_HOST', 'supplier-redis')
        self.redis_port = config.get('REDIS_PORT', 6379)
        self.redis_db = config.get('REDIS_DB', 0)
        self.redis_password = config.get('REDIS_PASSWORD', None)
        self.redis_pool = self.get_redis_pool()
        self.redis = None

        self.sm4_secret = config.get('SM4_SECRET', '')

    def get_singleton_kafka_producer(self):

        if self.kafka_enable != 'on':
            return None

        if not all([self.kafka_host, self.kafka_topic]):
            raise TiVendorError('KAFKA_HOST and KAFKA_TOPIC should be define in config')

        kafka_producers = self.__class__.kafka_producers

        if self.kafka_host in kafka_producers:
            return kafka_producers[self.kafka_host]

        kafka_producer = KafkaProducer(
            bootstrap_servers=self.kafka_host.split(','),
            # api_version=(0, 11, 0),
        )
        self.logger.info(f'New kafka_producer: {kafka_producer}')
        kafka_producers[self.kafka_host] = kafka_producer
        return kafka_producer

    def get_api_info(self, api_num):
        # 缓存 10 分钟
        
        v_redis = self.get_redis()
        key = f'config:exapi_info:{api_num}'
        info = v_redis.get(key)
        if info:
            return json.loads(info)

        url = self.tiadmin_host + '/supplier/services/'
        
        r = requests.get(url, params={'api_num': api_num})
        try:
            r = r.json()
        except Exception as e:
            self.logger.error('parse api info fault,status: %s,resp:%s' % (r.status_code, r.text), exc_info=True)
            raise e
        results = r.get('results')
        if not results:
            raise TiVendorError(f'{api_num} api not found')

        info = results[0]

        v_redis.set(key, json.dumps(info), 600)

        return info

    def request(self, api_num, service_name='', ti_request_headers=None, verify=False, **kwargs):
        info = self.get_api_info(api_num)
        url = info['url']
        method = info['method']
        timeout = float(info.get('timeout', 60))
        if timeout <= 0:
            timeout = 5
        self.logger.info(f'Vendor Request: {method}, {url}, {timeout}, {kwargs}')

        start_time = self.now_time()
        response = requests.request(method, url, timeout=timeout, verify=verify, **kwargs)
        end_time = self.now_time()

        # if self.kafka_producer:
        #
        #     service_name = service_name or self.default_service_name or self.get_service_name()
        #     ti_request_headers = ti_request_headers or self.get_ti_request_headers()
        #     kwargs.update({
        #         'instance': self,
        #         'api_info': info,
        #         'url': url,
        #         'method': method,
        #         'response': response,
        #         'start_time': start_time,
        #         'end_time': end_time,
        #         'ti_request_headers': ti_request_headers,
        #         'service_name': service_name,
        #     })
        #
        #     start_new_thread(kafka_push, args=(), kwargs=kwargs)

        return response, start_time, end_time, info

    def kafka_expush(self, info, response, start_time, end_time, service_name, ti_request_headers, **kwargs):
        if self.kafka_producer:
            url = info['url']
            method = info['method']

            service_name = service_name or self.default_service_name or self.get_service_name()
            ti_request_headers = ti_request_headers or self.get_ti_request_headers()
            kwargs.update({
                'instance': self,
                'api_info': info,
                'url': url,
                'method': method,
                'response': response,
                'start_time': start_time,
                'end_time': end_time,
                'ti_request_headers': ti_request_headers,
                'service_name': service_name,
            })

            # # 判断一下 kong_request_id 如果已经存在就不要重复推送
            # reqid = ti_request_headers.get('Kong-Request-Id', '')
            # for a in TiVendor.queue:
            #     # 为加快判断速度，可以先判断最近的几条记录，如果命中就不往下判断了
            #     for b in TiVendor.queue[-50:]:
            #         aid = a['ti_request_headers'].get('Kong-Request-Id', '')
            #         bid = b['ti_request_headers'].get('Kong-Request-Id', '')
            #         if aid == reqid:
            #             return
            #         if bid == reqid:
            #             return

            start_new_thread(kafka_push, args=(), kwargs=kwargs)

            TiVendor.queue.append(kwargs)

    def get_service_name(self):
        try:
            from flask import request
            path = request.path.strip('/')
            service_name = path.split('/')[1]
            return service_name
        except ImportError:
            pass
        # todo: support for more framework
        return ''

    def get_ti_request_headers(self):
        try:
            from flask import request
            return dict(request.headers)
        except ImportError:
            pass
        # todo: support for more framework
        return {}

    def now_time(self):
        return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def get_redis_pool(self):
        redis_pools = self.__class__.redis_pools

        if self.redis_host in redis_pools:
            return redis_pools[self.redis_host]

        redis_pool = redis.ConnectionPool(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password,
            db=self.redis_db
        )
        self.logger.info(f'New redis_pool: {redis_pool}')
        redis_pools[self.redis_host] = redis_pool
        return redis_pool

    def get_redis(self):
        if self.redis:
            return self.redis
        self.redis = redis.StrictRedis(connection_pool=self.redis_pool)
        return self.redis

    def get_datasource_config(self, key):
        v_redis = self.get_redis()
        cache_key = f'config:source:{key}'
        info = v_redis.get(cache_key)
        if info:
            return info

        url = self.tiadmin_host + '/supplier/source/'
        r = requests.get(url, params={'key': key}).json()
        results = r.get('results')
        if not results:
            raise TiVendorError(f'{key} datasource_config not  found')

        info = results[0]

        v_redis.set(cache_key, info.get('source'))

        return info.get('source')


def desensitization(data, sm4_secret):
    
    if '|' not in sm4_secret:
        return data

    user_md5, key = sm4_secret.split('|')
    if len(key) != 16:
        return data

    data = encrypt_ecb(data, key)
    data = user_md5 + '|' + data
    return data


def kafka_push(**kwargs):

    instance = kwargs['instance']
    
    api_info = kwargs['api_info']
    url = kwargs['url']
    method = kwargs['method']
    response = kwargs['response']
    start_time = kwargs['start_time']
    end_time = kwargs['end_time']
    ti_request_headers = kwargs['ti_request_headers']
    service_name = kwargs['service_name']

    url_parse = urlparse(url)
    
    assert isinstance(instance, TiVendor)
    
    request_body = kwargs.get('json', '') or kwargs.get('data', '') or kwargs.get('files', '')
    request_body = json.dumps(request_body) if isinstance(request_body, (dict, list)) else request_body
    request_body = desensitization(request_body, instance.sm4_secret)

    request_params = kwargs.get('params', '')
    request_params = json.dumps(request_params) if isinstance(request_params, (dict, list)) else request_params
    request_params = desensitization(request_params, instance.sm4_secret)
    
    body = {
        'start_time': start_time,
        'end_time': end_time,
        'kong_request_id': ti_request_headers.get('Kong-Request-Id', ''),
        'x_request_id': ti_request_headers.get('X-Request-Id', ''),
        'x_real_ip': ti_request_headers.get('X-Real-Ip', ''),
        'x_consumer_id': ti_request_headers.get('X-Consumer-Id', ''),
        'x_consumer_username': ti_request_headers.get('X-Consumer-Username', ''),
        'x_credential_username': ti_request_headers.get('X-Credential-Username', ''),
        'triple_url': url,
        'triple_host': '%s:%s' % (url_parse.hostname, url_parse.port) if url_parse.port else url_parse.hostname,
        'method': method,
        'request': {
            'headers': '',
            'params': request_params,
            'body': request_body,
        },
        'response': {
            'headers': '',
            'body': '',
        },
        'status_code': 499,
        'service_name': service_name,
        'api_num': api_info.get('api_num', ''),
        'supplier_name': '%s-%s-%s' % (
            api_info.get('org_name', 'empty'), api_info.get('product_name', 'empty'),
            api_info.get('product_defines', 'empty')),
    }

    if response is not None:
        body['request']['headers'] = json.dumps(dict(response.request.headers))
        body['response'] = {
            'headers': json.dumps(dict(response.headers)),
            'body': response.text,
        }
        body['status_code'] = response.status_code
    
    try:
        msg = json.dumps(body).encode('utf8')
        instance.kafka_producer.send(instance.kafka_topic, value=msg)
    except:
        instance.logger.error('kafka send error(%s)' % body['kong_request_id'], exc_info=True)

