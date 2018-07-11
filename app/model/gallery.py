from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from model import BaseModel


class GalleryModel(BaseModel):

    __tablename__ = 'gallery'

    path = Column(String)
    images = relationship('ImageModel', back_populates='gallery')
