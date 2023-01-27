import os


GALLERY_PATH = os.getenv("GALLERY_PATH", "/home/manti/www/mgallery/data")

REDIS_URL = "redis://localhost:6379/10"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(message)s %(filename)s:%(lineno)d",
            "datefmt": "%H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "debug_log": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": os.getenv(
                "DEBUG_LOG", "/home/manti/www/mgallery/logs/debug.log"
            ),
        },
        "error_log": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": os.getenv(
                "ERROR_LOG", "/home/manti/www/mgallery/logs/error.log"
            ),
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "debug_log", "error_log"],
            "level": "INFO",
            "propagate": True,
        }
    },
}
