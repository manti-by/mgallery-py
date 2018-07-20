import numpy as np


class Comparator:

    def __init__(self, descriptor, personalized):
        self.descriptor = descriptor
        self.personalized = personalized

    @staticmethod
    def is_descriptors_similar(dsc_1, dsc_2):
        """
        In general, if two face descriptor vectors have a Euclidean
        distance between them less than 0.6 then they are from the same
        person, otherwise they are from different people.
        """
        np_array_1 = np.asarray(list(dsc_1))
        np_array_2 = np.asarray(list(dsc_2))
        distance = np.linalg.norm(np_array_1 - np_array_2)
        return distance < 0.6

    @property
    def is_similar(self):
        return self.is_descriptors_similar(self.descriptor.vector,
                                           self.personalized.vector)
