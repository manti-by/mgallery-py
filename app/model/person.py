from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from model.base import BaseModel


class PersonModel(BaseModel):

    __tablename__ = 'person'

    name = Column(String)

    descriptors = relationship('DescriptorModel', back_populates='person')
