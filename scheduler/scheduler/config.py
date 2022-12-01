import os
import logging

from dotenv import load_dotenv


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()

PARSING_SERVICE_URL = os.getenv("SCRAPY_SERVER_URL", "")
SCHEDULER_INTERVAL = int(os.getenv("SCHEDULER_INTERVAL", 10))

KAFKA_SUBSCRIPTIONS_TOPIC = os.environ["KAFKA_SUBSCRIPTIONS_TOPIC"]
KAFKA_BOOTSTRAP_SERVER = os.environ["KAFKA_BOOTSTRAP_SERVER"]

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
