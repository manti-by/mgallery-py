from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from model import BaseModel


class ImageModel(BaseModel):

    __tablename__ = 'image'

    path = Column(String)
    phash = Column(String)

    camera = Column(String)
    lens = Column(String)
    datetime = Column(DateTime)
    location = Column(String)

    gallery_id = Column(Integer, ForeignKey('gallery.id'))
    gallery = relationship('GalleryModel', back_populates='images')
