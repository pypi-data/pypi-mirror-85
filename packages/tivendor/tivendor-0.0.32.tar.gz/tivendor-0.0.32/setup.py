from setuptools import setup


try:
    long_description = open('README.md', encoding='utf8').read()
except Exception as e:
    long_description = ''


setup(
    name='tivendor',
    version='0.0.32',
    description='vendor request of taiqiyun [private]',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.22.0',
        'kafka-python>=1.4.6',
        'redis>=3.3.11',
        'tisdk>=0.0.30',
    ],
    py_modules=['tivendor'],
    include_package_data=True,
)
