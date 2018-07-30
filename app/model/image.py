from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from model.base import BaseModel


class ImageModel(BaseModel):

    __tablename__ = 'image'

    path = Column(String)
    name = Column(String)
    phash = Column(String)

    camera = Column(String)
    lens = Column(String)
    datetime = Column(DateTime)
    location = Column(String)

    width = Column(Integer)
    height = Column(Integer)

    gallery_id = Column(Integer, ForeignKey('gallery.id'))
    gallery = relationship('GalleryModel', back_populates='images')

    descriptors = relationship('DescriptorModel', back_populates='image')
