import asyncio
import json
import logging

from aiohttp import ClientSession
from aiokafka import AIOKafkaConsumer

from config import (
    KAFKA_BOOTSTRAP_SERVER,
    KAFKA_SUBSCRIPTIONS_TOPIC,
    PARSING_SERVICE_URL,
    SCHEDULER_INTERVAL,
)

from domain.entities.user_setting import UserSetting
from db.repositories.user_settings import UserSettingsRepository

user_settings_repository = UserSettingsRepository()


async def schedule_job(session: ClientSession, setting: UserSetting):
    """
    Make request to scrapyd server for scraping jobs
    scheduling.
    """

    params = {"project": "scraper", "spider": "myhome.ge", "user_id": setting.user_id}

    try:
        async with session.post(url=PARSING_SERVICE_URL, data=params) as response:
            resp = await response.read()
            logging.info("Successfully scheduled job. %s", resp)
    except Exception as e:
        logging.exception(e)


async def schedule_all():
    user_settings = user_settings_repository.get_all()

    async with ClientSession() as session:
        ret = await asyncio.gather(
            *[schedule_job(session, setting) for setting in user_settings]
        )
    logging.info("Done. Scheduled %s jobs", len(ret))


async def start_scheduling():
    while True:
        await schedule_all()
        await asyncio.sleep(SCHEDULER_INTERVAL)


async def consume_subscriptions_kafka_messages():
    consumer = AIOKafkaConsumer(
        KAFKA_SUBSCRIPTIONS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
        value_deserializer=lambda message: json.loads(message.decode("utf-8")),
    )
    await consumer.start()
    try:
        async for msg in consumer:
            logging.info("Consumed new subscription: %s", msg.value)
            user_settings_repository.add(
                setting=UserSetting(user_id=msg.value["user_id"])
            )

    finally:
        await consumer.stop()


async def main():
    await asyncio.gather(consume_subscriptions_kafka_messages(), start_scheduling())


if __name__ == "__main__":
    asyncio.run(main())
