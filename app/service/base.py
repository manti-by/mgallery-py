from sqlalchemy import text
from core.app import app
from service.exception import MissingRequiredField, ModelNotSetException


class BaseService:

    model = None

    def __init__(self):
        if self.model is None:
            raise ModelNotSetException("Model not set for %s" % self.__class__)

        self.session = app.db.session

    def create(self, **kwargs):
        model_instance = self.model(**kwargs)

        self.session.add(model_instance)
        self.session.commit()

        return model_instance.id

    def update(self, **kwargs):
        if "id" not in kwargs.keys():
            raise MissingRequiredField("Field id not set for %s" % self.__class__)

        model_instance = self.model(**kwargs)

        self.session.merge(model_instance)
        self.session.commit()

        return kwargs.get("id")

    def get(self, **kwargs):
        return self.list(**kwargs).first()

    def list(self, **kwargs):
        return (
            self.session.query(self.model)
            .filter_by(**kwargs)
            .order_by(text("created_at desc"))
        )

    def delete(self, obj, commit=True):
        self.session.delete(obj)
        if commit:
            self.session.commit()

    def add(self, obj, commit=True):
        self.session.add(obj)
        if commit:
            self.session.commit()

    def add_all(self, objects, commit=True):
        self.session.add_all(objects)
        if commit:
            self.session.commit()
