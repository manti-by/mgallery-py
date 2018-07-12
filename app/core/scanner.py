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
        logger.debug('Start scanning %s' % self.path)

        gallery_list = {
            x.path: x.id
            for x in self.gallery.list()
        }
        for r, rd, rf in os.walk(self.path):
            for current_directory in rd:
                dir_name = os.path.dirname(current_directory)
                if dir_name in ['__pycache__']:
                    continue

                if current_directory not in gallery_list.keys():
                    gallery_id = self.gallery.create(path=current_directory)
                    logger.debug('Added gallery %s' % current_directory)
                else:
                    gallery_id = gallery_list[current_directory]

                image_list = {
                    x.path: x.id
                    for x in self.image.list(gallery_id=gallery_id)
                }
                for c, cd, cf in os.walk(os.path.join(r, current_directory)):
                    for current_file in cf:
                        file_name, file_ext = os.path.splitext(current_file)
                        if file_ext not in ['.jpg', '.jpeg', '.png']:
                            continue

                        file_path = os.path.join(current_directory, current_file)
                        if file_path not in image_list.keys():
                            self.image.create(path=file_path, gallery_id=gallery_id)
                            logger.debug('Added image %s ' % current_file)

        logger.debug('Finish scanning')
