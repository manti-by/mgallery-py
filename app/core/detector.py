import dlib
import logging
import numpy as np

from core.conf import settings

logger = logging.getLogger()


class Detector:

    detects = []
    landmarks = []

    scores = []
    face_types = []

    def __init__(self, path, debug=False):
        self.path = path

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(settings['predictor'])

        rgb_image = dlib.load_rgb_image(path)
        grey_image = np.mean(rgb_image, -1)
        self.image = grey_image.astype(np.uint8)

        self.debug = debug
        if self.debug:
            self.window = dlib.image_window()
            self.window.clear_overlay()

    @staticmethod
    def shape_to_array(shape):
        array = np.zeros((68, 2), dtype=np.int)
        for i in range(0, 68):
            array[i] = (shape.part(i).x, shape.part(i).y)
        return array

    def detect_faces(self):
        self.detects, self.scores, self.face_types = self.detector.run(self.image, 1)
        logger.debug('Number of faces detected: %d' % len(self.detects))

    def build_landmarks(self):
        for (i, rectangle) in enumerate(self.detects):
            landmark = self.predictor(self.image, rectangle)
            self.landmarks.append(landmark)
        logger.debug('Number of landmarks built: %d' % len(self.detects))

    def run(self):
        logger.debug('Start analyzing image %s' % self.path)

        self.detect_faces()
        self.build_landmarks()

        if self.debug:
            self.window.set_image(self.image)
            self.window.add_overlay(self.detects, dlib.rgb_pixel(255, 0, 0))
            self.window.add_overlay(self.landmarks, dlib.rgb_pixel(0, 255, 0))
            dlib.hit_enter_to_continue()

        logger.debug('Finish analyzing')
