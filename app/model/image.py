from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from model import BaseModel


class ImageModel(BaseModel):

    __tablename__ = 'image'

    path = Column(String)
    phash = Column(String)

    gallery_id = Column(Integer, ForeignKey('gallery.id'))
    gallery = relationship('GalleryModel', back_populates='images')
