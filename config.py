import os
from functools import lru_cache


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    DATABASE_URL = (f'postgresql://'
                    f'{os.getenv("POSTGRES_USER")}:'
                    f'{os.getenv("POSTGRES_PASSWORD")}@'
                    f'{os.getenv("POSTGRES_HOST")}:'
                    f'{os.getenv("POSTGRES_PORT")}/'
                    f'{os.getenv("POSTGRES_DB")}')
    DATABASE_CONNECT_DICT: dict = {}


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
