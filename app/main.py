import argparse
import logging
import logging.config

from core import version
from core.conf import settings
from core.detector import Detector
from core.scanner import Scanner


logging.basicConfig(level=logging.DEBUG)
logging.config.dictConfig(settings['logging'])


parser = argparse.ArgumentParser(
    prog='MGallery',
    description='Custom gallery engine with AI features.',
    add_help=True
)

parser.add_argument('-v', '--verbose',
                    action='count',
                    help='Increase output verbosity')

parser.add_argument('--version',
                    action='version',
                    version=version,
                    help='Print application version')

parser.add_argument('-s', '--scan',
                    dest='gallery', nargs='?', const=settings['gallery'],
                    help='Scan gallery for images')

parser.add_argument('-d', '--detect',
                    dest='image', nargs='?', const=settings['image'],
                    help='Scan gallery for images')

parser.add_argument('-w', '--window',
                    action='count',
                    help='Show result window')


if __name__ == '__main__':
    args = parser.parse_args()

    if args.gallery is not None:
        scanner = Scanner(args.gallery)
        scanner.run()
    elif args.image is not None:
        detector = Detector(args.image, args.window > 0)
        detector.run()
    else:
        parser.print_help()
