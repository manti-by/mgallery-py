import os


def project_path(path):
    return os.path.abspath(os.path.join(
        os.path.abspath(__file__), '..', '..', '..', path
    ))


def path_param(param, path):
    return os.getenv(param, project_path(path))


settings = {
    'gallery': path_param('GALLERY_PATH', 'gallery'),
    'predictor': path_param(
        'PREDICTOR_PATH', 'models/shape_predictor_68_face_landmarks.dat'
    ),
    'recognizer': path_param(
        'RECOGNIZER_PATH', 'models/dlib_face_recognition_resnet_model_v1.dat'
    ),
    'database': os.getenv(
        'DATABASE_URL', 'postgresql://mgallery:pa55word@mgallery-postgres/mgallery'
    ),
    'test_database': os.getenv(
        'TEST_DATABASE_URL', 'postgresql://mgallery:pa55word@mgallery-postgres-test/mgallery'
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
