import logging
from logging.config import dictConfig
from jsonformatter import JsonFormatter

def setup(config=None):
    """Config must contains logging field. e.g.
        {
            "logging": {

            }
        }
    """
    logfile = config.get("logfile", "app.log")
    loglevel = config.get("loglevel", "INFO")
    logfmt = config.get("logfmt", "json")

    config = config or {}
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "{asctime} {levelname} {pathname} {lineno} {module} {funcName} {process} {thread} {message}",
                "style": "{"
            },
            "json": {
                "class": "jsonformatter.JsonFormatter",
                "format": {
                    "asctime": "asctime",
                    "levelname": "levelname",
                    "pathname": "pathname",
                    "lineno": "lineno",
                    "module": "module",
                    "funcName": "funcName",
                    "process": "process",
                    "thread": "thread",
                    "message": "message",
                },
            },
        },
        "handlers": {
            "default_console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "default_file": {
                "level": "DEBUG",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": logfile,
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "formatter": "default",
            },
            "json_console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
            "json_file": {
                "level": "DEBUG",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": logfile,
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "formatter": "json",
            },
        },
        "loggers": {
        },
        "root": {
            "handlers": [logfmt+"_file", logfmt+"_console"],
            "level": loglevel,
            "propagate": True,
        }
    }
    logging_config.update(config.get("logging", {}))
    dictConfig(logging_config)
