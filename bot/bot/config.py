import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

KAFKA_BOOTSTRAP_SERVERS = [os.getenv("KAFKA_BOOTSTRAP_SERVER")]
KAFKA_APARTMENTS_TOPIC = os.getenv("KAFKA_APARTMENTS_TOPIC")
KAFKA_SUBSCRIPTIONS_TOPIC = os.getenv("KAFKA_SUBSCRIPTIONS_TOPIC")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
