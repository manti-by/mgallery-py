import os
import glob
import logging

from core.celery import (
    process_gallery,
    process_image,
    find_faces
)
from service import (
    GalleryService,
    ImageService
)

logger = logging.getLogger()


class Scanner:

    def __init__(self, path):
        self.path = path
        self.gallery = GalleryService()
        self.image = ImageService()

    @property
    def file_list(self):
        files = []
        for ext in ['**/*.jpg', '**/*.jpeg', '**/*.png']:
            files.extend(glob.glob(os.path.join(self.path, ext), recursive=True))
        return files

    def run(self):
        logger.debug('Start scanning %s' % self.path)

        gallery_list = {
            x.path: x.id
            for x in self.gallery.list()
        }
        for current_file in self.file_list:
            current_directory = os.path.dirname(current_file)
            if current_directory not in gallery_list.keys():
                gallery_id = self.gallery.create(path=current_directory)
                gallery_list[current_directory] = gallery_id

                process_gallery.delay(gallery_id)

                logger.debug('Added gallery %s' % current_directory)
            else:
                gallery_id = gallery_list[current_directory]

            image_list = {
                x.path: x.id
                for x in self.image.list(gallery_id=gallery_id)
            }
            if current_file not in image_list.keys():
                image_id = self.image.create(path=current_file, gallery_id=gallery_id)
                image_list[current_file] = image_id

                process_image.delay(image_id)
                find_faces.delay(image_id)

                logger.debug('Added image %s ' % current_file)

        logger.debug('Finish scanning')
