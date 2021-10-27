import os


GALLERY_PATH = os.getenv("GALLERY_PATH", "/home/manti/www/mgallery/photo/")

DATABASE_PATH = os.getenv("DATABASE_PATH", "/home/manti/www/mgallery/db.sqlite")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

QUEUES = ("mgallery",)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "%H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "debug_log": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.getenv("DEBUG_LOG", "/home/manti/www/mgallery/debug.log"),
        },
        "error_log": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.getenv("ERROR_LOG", "/home/manti/www/mgallery/error.log"),
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "debug_log", "error_log"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}
