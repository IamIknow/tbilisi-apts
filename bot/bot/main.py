import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from telegram import Update, Bot, InputMediaPhoto
from telegram.constants import ParseMode
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


def get_message_layout(apartment) -> str:
    text = f"""Price: {apartment["price"]} $
    Area: {apartment["size"]}
    Link: <a href=\"{apartment["link"]}\">Link</a>"""
    return text


async def send_apartment_photos(apartment) -> None:
    photos = [
        InputMediaPhoto(image_link) for image_link in apartment["image_links"][:5]
    ]
    try:
        await bot.send_media_group(chat_id=apartment["user_id"], media=photos)
    except Exception as e:
        logging.exception(e)


async def send_apartment_text(apartment) -> None:
    try:
        await bot.send_message(
            text=get_message_layout(apartment),
            chat_id=apartment["user_id"],
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        logging.exception(e)


async def send_apartment_message(apartment) -> None:
    await send_apartment_photos(apartment)
    await send_apartment_text(apartment)


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
            await send_apartment_message(apartment=message.value)
    finally:
        logging.info("Stopping the consumer...")
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
