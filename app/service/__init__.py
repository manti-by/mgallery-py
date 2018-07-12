from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.conf import settings
from service.exception import (
    MissingRequiredField,
    ModelNotSetException,
)


class BaseService:

    model = None

    def __init__(self):
        if self.model is None:
            raise ModelNotSetException('Model not set for %s' % self.__class__)

        self.db = sessionmaker(
            bind=create_engine(settings['database'])
        )()

    def create(self, **kwargs):
        model_instance = self.model(**kwargs)

        self.db.add(model_instance)
        self.db.commit()

        return model_instance.id

    def update(self, **kwargs):
        if 'id' not in kwargs.keys():
            raise MissingRequiredField('Field id not set for %s' % self.__class__)

        model_instance = self.model(**kwargs)

        self.db.merge(model_instance)
        self.db.commit()

        return kwargs.get('id')

    def get(self, **kwargs):
        return self.list(**kwargs).first()

    def list(self, **kwargs):
        return self.db \
            .query(self.model).filter_by(**kwargs)
