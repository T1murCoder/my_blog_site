import telebot
import time
import logging
import logging.config
import requests
import json
from dotenv import load_dotenv
import os

telebot.apihelper.ENABLE_MIDDLEWARE = True

with open("channels_id.json") as f:
    valid_channels_ids = json.load(f)['ids']


load_dotenv()
API_TOKEN = os.getenv('TELEBOT_TOKEN')
website_api_token = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)


def get_logging_dict_config():
    return {
        "version": 1,
        "formatters": {
            "detailed": {
                "format": "[%(asctime)s] - %(name)s:%(module)s:%(lineno)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "formatter": "detailed",
                "filename": "../logs/tg_bot_logs.log"
            }
        },
        "loggers": {
            "tg_bot": {
                "handlers": ["file"],
                "level": "INFO"
            }
        }
    }


logging.config.dictConfig(get_logging_dict_config())
logger = logging.getLogger("tg_bot")


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """Здравствуй! Я бот созданный для парсинга телеграм каналов""")


@bot.middleware_handler(update_types=['channel_post', 'edited_channel_post'])
def update_handler(bot_instance, channel_post):
    if channel_post.chat.id not in valid_channels_ids:
        return
    post_tg_url = "http://t.me/" + channel_post.chat.username
    message_id = channel_post.id
    post_tg_url += "/" + str(message_id)
    make_request(post_tg_url)
    time.sleep(1)
        

def make_request(url):
    try:
        response = requests.post(f"http://localhost:8080/api/v2/posts/token={website_api_token}", json={'url': url})
        if response:
            logger.info(f"Succesfuly posted: url={url}")
        else:
            logger.info(f"Bad gateway: url={url}")
    except Exception as ex:
        logger.error(f"Connection Error: url={url}")
        print(ex)


bot.infinity_polling()