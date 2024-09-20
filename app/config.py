import os

DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_NAME = os.environ.get('DATABASE_NAME')


SYNC_DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@db:5432/{DATABASE_NAME}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@db:5432/{DATABASE_NAME}"
TEST_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@db:5432/{DATABASE_NAME}"

YANDEX_SPELLER_URL = "https://speller.yandex.net/services/spellservice.json/checkText"

SECRET_KEY = os.environ.get('SECRET_KEY')
