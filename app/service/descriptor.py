from model.descriptor import DescriptorModel
from service import BaseService


class DescriptorService(BaseService):

    model = DescriptorModel

    def personalized(self):
        return self.db \
            .query(self.model).filter(self.model.person_id is not None)
