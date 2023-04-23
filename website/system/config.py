from flask import request, has_request_context
import logging


url = "http://localhost:8080/"


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


def get_logging_dict_config():
    return {
        "version": 1,
        "formatters": {
            "detailed": {
                "()": CustomFormatter,
                "format": "%(remote_addr)s - %(url)s - - [%(asctime)s] - %(name)s:%(module)s:%(lineno)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "detailed",
                "filename": "logs/logs.log",
                'maxBytes': 10485760,
                'backupCount': 5,
            }
        },
        "loggers": {
            "app": {
                "handlers": ["file"],
                "level": "INFO"
            }
        }
    }