from sqlalchemy import Column, Integer, ForeignKey, ARRAY,  Float
from sqlalchemy.orm import relationship

from model import BaseModel


class DescriptorModel(BaseModel):

    __tablename__ = 'descriptor'

    vector = Column(ARRAY(Float))

    image_id = Column(Integer, ForeignKey('image.id'))
    image = relationship('ImageModel', back_populates='descriptors')

    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('PersonModel', back_populates='descriptors')
