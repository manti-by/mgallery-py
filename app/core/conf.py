import os

GALLERY_PATH = os.getenv(
    'GALLERY_PATH', os.path.abspath(os.path.join(
        os.path.abspath(__file__), '..', '..', '..', 'gallery'
    ))
)

PREDICTOR_PATH = os.getenv(
    'PREDICTOR_PATH', os.path.abspath(os.path.join(
        os.path.abspath(__file__), '..', '..', '..',
        'deploy', 'conf', 'shape_predictor_68_face_landmarks.dat'
    ))
)


settings = {
    'gallery': GALLERY_PATH,
    'image': os.path.join(
        GALLERY_PATH, 'face-detection.jpg'
    ),
    'predictor': PREDICTOR_PATH,
    'database': os.getenv(
        'DATABASE_URL', 'postgresql://mgallery:pa55word@mgallery-postgres/mgallery'
    ),
    'celery_broker': os.getenv(
        'REDIS_URL', 'redis://mgallery-redis:6379/0'
    ),
    'logging': {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(message)s',
                'datefmt': '%H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    }
}
