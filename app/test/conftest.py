import logging
import logging.config

from core.conf import settings
from model.descriptor import DescriptorModel
from model.gallery import GalleryModel
from model.image import ImageModel
from model.person import PersonModel


logging.basicConfig(level=logging.DEBUG)
logging.config.dictConfig(settings['logging'])
