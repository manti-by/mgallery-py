import argparse
import logging

from core import version
from core.admin import run_server
from core.celery import find_duplicates
from core.conf import settings
from core.scanner import Scanner
from core.utils import setup_logging
from service.image import ImageService

parser = argparse.ArgumentParser(
    prog="python main.py", description="Custom gallery engine.", add_help=True
)

parser.add_argument("-a", "--admin", action="store_true", help="Run admin panel")

parser.add_argument("-m", "--merge", action="store_true", help="Merge duplicate images")

parser.add_argument(
    "-s",
    "--scan",
    dest="scan",
    nargs="?",
    const=settings["gallery"],
    help="Scan gallery for images",
)

parser.add_argument(
    "-v", "--verbose", action="count", default=3, help="Increase output verbosity"
)

parser.add_argument(
    "--version", action="version", version=version, help="Print application version"
)


if __name__ == "__main__":
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger()

    if args.admin:
        run_server()
    elif args.merge:
        for image in ImageService().list():
            find_duplicates.delay(image.id)
    elif args.scan is not None:
        scanner = Scanner(args.scan)
        scanner.run()
    else:
        parser.print_help()
