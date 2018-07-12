import os
import logging

from service.gallery import GalleryService
from service.image import ImageService

logger = logging.getLogger()


class Scanner:

    def __init__(self, path):
        self.path = path
        self.gallery = GalleryService()
        self.image = ImageService()

    def run(self):
        gallery_list = {
            x.path: x.id
            for x in self.gallery.list()
        }

        # TODO: Add filters
        for r, rd, rf in os.walk(self.path):
            for current_directory in rd:
                if current_directory not in gallery_list.keys():
                    gallery_id = self.gallery.create(path=current_directory)
                    logger.debug('Added gallery %s' % current_directory)
                else:
                    gallery_id = gallery_list[current_directory]

                for c, cd, cf in os.walk(os.path.join(r, current_directory)):
                    for current_file in cf:
                        file_name = os.path.join(current_directory, current_file)
                        self.image.create(path=file_name, gallery_id=gallery_id)
                        logger.debug('Added image %s ' % current_file)
