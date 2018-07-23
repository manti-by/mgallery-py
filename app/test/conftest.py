import logging
import logging.config

from core.conf import settings
from model import (
    DescriptorModel,
    GalleryModel,
    ImageModel,
    PersonModel
)


logging.basicConfig(level=logging.DEBUG)
logging.config.dictConfig(settings['logging'])
