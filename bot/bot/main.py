import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from telegram import Update, Bot
from telegram.ext import CommandHandler, ContextTypes, ApplicationBuilder, Application

from config import (
    KAFKA_APARTMENTS_TOPIC,
    KAFKA_SUBSCRIPTIONS_TOPIC,
    KAFKA_BOOTSTRAP_SERVERS,
    TELEGRAM_BOT_TOKEN,
)


bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def init_producer() -> None:
    # TODO Remove global
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )
    await producer.start()


async def consume_apartments_kafka_messages() -> None:
    consumer = AIOKafkaConsumer(
        KAFKA_APARTMENTS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda message: json.loads(message.decode("utf-8")),
    )
    await consumer.start()

    try:
        async for message in consumer:
            logging.info("key=%s value=%s" % (message.key, message.value))
            await bot.send_message(
                text=message.value["link"], chat_id=message.value["user_id"]
            )

    finally:
        await consumer.stop()


async def initialize_kafka(_app: Application) -> None:
    await init_producer()
    asyncio.create_task(consume_apartments_kafka_messages())


async def send_subscription_event(chat_id: int):
    await producer.send_and_wait(KAFKA_SUBSCRIPTIONS_TOPIC, {"user_id": chat_id})


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot Activated. You will receive updates now.")
    await send_subscription_event(update.message.chat_id)


def start_bot_polling() -> None:
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.post_init = initialize_kafka

    app.run_polling()


if __name__ == "__main__":
    start_bot_polling()
