from jinja2 import Markup
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from model.base import BaseModel


class GalleryModel(BaseModel):

    __tablename__ = "gallery"

    path = Column(String)
    year = Column(String)

    images = relationship("ImageModel", back_populates="gallery")

    @property
    def url(self):
        return Markup('<a href="/gallery/{}/">{}</a>'.format(self.id, self.year))

    @property
    def cover(self):
        return self.images[-1]
