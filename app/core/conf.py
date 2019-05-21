import os

settings = {
    "gallery": os.getenv(
        "GALLERY_PATH", "/media/gallery/"
    ),
    "database": os.getenv(
        "DATABASE_URL", "postgresql://mgallery:pa55word@mgallery-postgres:5432/mgallery"
    ),
    "celery_broker": os.getenv(
        "REDIS_URL", "redis://mgallery-redis:6379/0"
    ),
    "logging": {
        "version": 1,
        "disable_existing_loggers": True,
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
            }
        },
        "loggers": {"": {"handlers": ["console"], "level": "DEBUG", "propagate": True}},
    },
}
