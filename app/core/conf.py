import os

settings = {
    "host": os.getenv("FLASK_HOST", "0.0.0.0"),
    "port": os.getenv("FLASK_PORT", 8808),
    "flower_url": os.getenv("FLOWER_URL", "https://mx.manti.by/flower/"),
    "gallery": os.getenv("GALLERY_PATH", "/var/lib/mgallery/"),
    "database": os.getenv(
        "DATABASE_URL", "postgresql://mgallery:pa55word@mgallery-postgres:5432/mgallery"
    ),
    "celery_broker": os.getenv("REDIS_URL", "redis://mgallery-redis:6379/0"),
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
