from sqlalchemy import desc, func

from model import GalleryModel, ImageModel
from service import BaseService


class GalleryService(BaseService):

    model = GalleryModel

    def admin_queryset(self):
        self.session.query(
            self.model.path.label("path"),
            func.count(ImageModel.id).label("image_count"),
        ).join(ImageModel).group_by(self.model.id)

    def list(self, **kwargs):
        return (
            self.session.query(self.model)
            .filter_by(**kwargs)
            .join(ImageModel)
            .order_by(desc(ImageModel.created_at))
        )
