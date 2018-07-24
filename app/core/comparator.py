import numpy as np

from service import DescriptorService


class Comparator:

    def __init__(self, descriptor):
        self.descriptor = descriptor

    @staticmethod
    def is_similar(dsc_1, dsc_2):
        """
        In general, if two face descriptor vectors have a Euclidean
        distance between them less than 0.6 then they are from the same
        person, otherwise they are from different people.
        """
        np_array_1 = np.asarray(list(dsc_1))
        np_array_2 = np.asarray(list(dsc_2))
        distance = np.linalg.norm(np_array_1 - np_array_2)
        return distance < 0.6

    def find_person(self):
        for personalized in DescriptorService().personalized():
            if self.is_similar(self.descriptor.vector,
                               personalized.vector):
                return personalized.person_id
