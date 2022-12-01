# Bot

Telegram bot which consumes messages from kafka topic and posts them to users.

## Run locally

Before first run you should create the .env file in the service's root directory. Use .env.example file for list of variables that must be set.

```
source .env && python ./bot/main.py
```
