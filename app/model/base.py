from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base


class Base(object):

    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return "<%s('%s')>" % (self.__class__, self.id)


BaseModel = declarative_base(cls=Base)
