import os
from dotenv import load_dotenv

load_dotenv()

LOCAL_MODE = os.getenv("LOCAL_MODE")

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
REDIS_URL = os.getenv("REDIS_URL")

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("POSTGRES_DB")
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_URI = f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
ADMIN_ID = os.getenv("ADMIN_ID")
