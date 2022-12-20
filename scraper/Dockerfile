# TODO: Change base image to slim or use miltistage build to reduce image size
FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml /app 
COPY README.md /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY ./scrapy.cfg /app
COPY ./setup.py /app
COPY ./scrapyd.conf /app
COPY ./run-scrapy-server.sh /app

RUN chmod +x ./run-scrapy-server.sh

COPY ./scraper /app/scraper

EXPOSE 6800

CMD [ "./run-scrapy-server.sh" ]
