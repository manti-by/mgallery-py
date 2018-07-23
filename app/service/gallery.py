from sqlalchemy import func

from model import (
    GalleryModel, ImageModel
)
from service import BaseService


class GalleryService(BaseService):

    model = GalleryModel

    def admin_queryset(self):
        self.db.query(
            GalleryModel.path.label('path'),
            func.count(ImageModel.id).label('image_count')
        ).join(
            ImageModel
        ).group_by(
            GalleryModel.id
        )
