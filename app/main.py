import argparse
import logging

from core import version
from core.admin import run_server
from core.conf import settings
from core.comparator import Comparator
from core.detector import Detector
from core.scanner import Scanner
from core.utils import setup_logging


parser = argparse.ArgumentParser(
    prog='python main.py',
    description='Custom gallery engine with AI features.',
    add_help=True
)

parser.add_argument('-c', '--compare',
                    nargs=2, metavar='IMAGE',
                    help='Detect and compare faces on two images')

parser.add_argument('-d', '--detect',
                    dest='image', nargs='?', const=settings['image'],
                    help='Detect faces on image (use with -w option for visualisation)')

parser.add_argument('-a', '--admin',
                    action='store_true',
                    help='Run admin panel')

parser.add_argument('-s', '--scan',
                    dest='gallery', nargs='?', const=settings['gallery'],
                    help='Scan gallery for images')

parser.add_argument('-w', '--window',
                    action='store_true',
                    help='Show result window for detector mode')

parser.add_argument('-v', '--verbose',
                    action='count',
                    help='Increase output verbosity')

parser.add_argument('--version',
                    action='version',
                    version=version,
                    help='Print application version')


if __name__ == '__main__':
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger()

    if args.gallery is not None:
        scanner = Scanner(args.gallery)
        scanner.run()
    elif args.image is not None:
        detector = Detector(args.image, args.window)
        detector.run()
    elif args.compare is not None:
        def find_similar(dsc_list_1, dsc_list_2):
            for dsc_1 in dsc_list_1:
                for dsc_2 in dsc_list_2:
                    if Comparator.is_descriptors_similar(dsc_1, dsc_2):
                        yield dsc_1, dsc_2

        logger.info('Checking similar faces on two images')

        dt_1 = Detector(args.compare[0])
        dt_1.run()

        dt_2 = Detector(args.compare[1])
        dt_2.run()

        similar = find_similar(dt_1.descriptors, dt_2.descriptors)
        logger.info('Found %d similar faces' % len(list(similar)))
    elif args.admin is not None:
        run_server()
    else:
        parser.print_help()
