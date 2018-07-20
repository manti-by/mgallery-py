from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from model import BaseModel


class PersonModel(BaseModel):

    __tablename__ = 'person'

    name = Column(String)

    descriptors = relationship('DescriptorModel', back_populates='person')
