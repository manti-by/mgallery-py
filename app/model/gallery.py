from jinja2 import Markup
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from model.base import BaseModel


class GalleryModel(BaseModel):

    __tablename__ = "gallery"

    path = Column(String)
    name = Column(String)

    images = relationship("ImageModel", back_populates="gallery", order_by="ImageModel.created_at.desc()")

    @property
    def url(self):
        return Markup('<a href="/gallery/{}/">{}</a>'.format(self.id, self.name))

    @property
    def cover(self):
        return self.images[1]
