import os
from functools import lru_cache
from environs import Env

env = Env()
env.read_env()


class BaseConfig:
    SECRET_KEY = env('SECRET_KEY')

    DATABASE_URL = (f'postgresql://'
                    f'{env("POSTGRES_USER")}:'
                    f'{env("POSTGRES_PASSWORD")}@'
                    f'{env("POSTGRES_HOST")}:'
                    f'{env("POSTGRES_PORT")}/'
                    f'{env("POSTGRES_DB")}')
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
    config_name = env('FASTAPI_CONFIG', default='development')
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
