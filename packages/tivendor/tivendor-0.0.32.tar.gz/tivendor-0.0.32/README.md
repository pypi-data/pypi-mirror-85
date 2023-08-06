# tivendor


### Usage
```
from tivendor import TiVendor

config =  {
    'TIADMIN_HOST': os.getenv('TIADMIN_HOST', 'http://tiadmin.kong:8000'),
    'KAFKA_HOST': os.getenv('KAFKA_HOST', 'kafka-kafka.kafka:9092'),
    'KAFKA_TOPIC': os.getenv('KAFKA_TOPIC', 'supplier-request'),
    'KAFKA_ENABLE': os.getenv('KAFKA_ENABLE', 'on'),
    'DEFAULT_SERVICE_NAME': os.getenv('DEFAULT_SERVICE_NAME', 'default_service_name'),
    'LOGGER_NAME': os.getenv('LOGGER_NAME', 'main'),
    'REDIS_HOST': os.getenv('REDIS_HOST', 'supplier-redis'),
    'REDIS_PORT': os.getenv('REDIS_PORT', 6379),
    'REDIS_DB': os.getenv('REDIS_DB', 0),
    'REDIS_PASSWORD': os.getenv('REDIS_PASSWORD', None),
    'SM4_SECRET': os.getenv('SM4_SECRET', ''),  # 可以通过调用 api 获取
}
vendor = TiVendor(config)

r = vendor.request('bqsblmatch-test', service_name='bqsblmatch', ti_request_headers={}, json={'name': 'Johnny',})
print(r.json())

```


