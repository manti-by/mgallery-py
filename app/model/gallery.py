from jinja2 import Markup
from sqlalchemy import Column, String, Date, SmallInteger
from sqlalchemy.orm import relationship

from model.base import BaseModel


class GalleryModel(BaseModel):

    __tablename__ = 'gallery'

    path = Column(String)
    name = Column(String)
    date = Column(Date)
    year = Column(SmallInteger)

    images = relationship('ImageModel', back_populates='gallery')

    @property
    def url(self):
        return Markup(
            '<a href="/gallery/{}/">{}</a>'.format(self.id, self.name)
        )
