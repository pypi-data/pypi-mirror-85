import os


class Config(object):
    ZK_NAMESPACE = os.environ.get('ZK_NAMESPACE', 'basic')
    ZK_HOSTS = os.environ.get('ZK_HOSTS', 'localhost:2181')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'for_dev')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@127.0.0.1/tele_coworker')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENABLED_RECORDER = os.environ.get('ENABLED_RECORDER', False)
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', True)
