from sqlalchemy import Column, String, Date, SmallInteger
from sqlalchemy.orm import relationship

from model import BaseModel


class GalleryModel(BaseModel):

    __tablename__ = 'gallery'

    path = Column(String)
    name = Column(String)
    date = Column(Date)
    year = Column(SmallInteger)

    images = relationship('ImageModel', back_populates='gallery')
