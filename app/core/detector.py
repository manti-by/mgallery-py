import dlib
import numpy
import logging

from core.conf import settings

logger = logging.getLogger()


class Detector:

    detects = []
    landmarks = []

    scores = []
    face_types = []

    def __init__(self, path):
        self.path = path
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(settings['predictor'])
        self.image = dlib.load_rgb_image(path)

    @staticmethod
    def shape_to_array(shape):
        array = numpy.zeros((68, 2), dtype='int')
        for i in range(0, 68):
            array[i] = (shape.part(i).x, shape.part(i).y)
        return array

    def detect_faces(self):
        self.detects, self.scores, self.face_types = self.detector.run(self.image, 1)
        logger.debug('Number of faces detected: %d' % len(self.detects))

    def build_landmarks(self):
        for (i, rectangle) in enumerate(self.detects):
            shape = self.predictor(self.image, rectangle)
            self.landmarks.append(
                self.shape_to_array(shape)
            )
        logger.debug('Number of landmarks built: %d' % len(self.detects))

    def run(self):
        logger.debug('Start analyzing image %s' % self.path)

        self.detect_faces()
        self.build_landmarks()

        logger.debug('Finish analyzing')
