import asyncio

from aiohttp import ClientSession
from logger import logger


SCRAPY_SERVER_URL = "http://localhost:6800/schedule.json"
SCHEDULER_INTERVAL = 30


async def schedule_job(session: ClientSession):
    """
    Make request to scrapyd server for scraping jobs
    scheduling.

    TODO: Make it work with stored data.
    """

    params = {"project": "scraper", "spider": "myhome.ge"}

    try:
        async with session.post(url=SCRAPY_SERVER_URL, data=params) as response:
            resp = await response.read()
            logger.info("Successfully scheduled job. %s", resp)
    except Exception as e:
        logger.exception(e)


async def schedule_all():
    async with ClientSession() as session:
        ret = await asyncio.gather(*[schedule_job(session)])
    logger.info("Done. Scheduled %s jobs", len(ret))


async def main():
    while True:
        await schedule_all()
        await asyncio.sleep(10)


asyncio.run(main())
