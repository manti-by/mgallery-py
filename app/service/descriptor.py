from model import DescriptorModel
from service import BaseService


class DescriptorService(BaseService):

    model = DescriptorModel

    def personalized(self):
        return self.session \
            .query(self.model).filter(self.model.person_id.isnot(None))
