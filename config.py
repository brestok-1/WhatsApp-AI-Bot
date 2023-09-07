import os
from functools import lru_cache

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopementConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


@lru_cache()
def get_settings() -> DevelopementConfig | ProductionConfig | TestingConfig:
    config_cls_dict = {
        'development': DevelopementConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    config_name = os.getenv('FASTAPI_CONFIG', default='development')
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
