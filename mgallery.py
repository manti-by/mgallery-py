import argparse

from mgallery.queue import queue
from mgallery.settings import GALLERY_PATH
from mgallery.utils import setup_logging

parser = argparse.ArgumentParser(
    prog="python mgallery.py", description="Image deduplicate script.", add_help=True
)

parser.add_argument(
    "-c", "--clean", action="store_true", default=False, help="Clean RQ queue"
)
parser.add_argument(
    "-m",
    "--merge",
    action="store_true",
    default=False,
    help="Merge duplicate images (Dry run without `--delete` key)",
)
parser.add_argument(
    "-d",
    "--delete",
    action="store_true",
    default=False,
    help="Delete duplicates from file system and database",
)
parser.add_argument(
    "-s",
    "--scan",
    dest="scan",
    nargs="?",
    const=GALLERY_PATH,
    help="Scan gallery for images [PATH_TO_GALLERY]",
)
parser.add_argument(
    "-v", "--verbose", action="count", default=3, help="Increase output verbosity"
)


if __name__ == "__main__":
    args = parser.parse_args()

    setup_logging(args.verbose)

    if args.clean:
        queue.empty()
    elif args.merge:
        from mgallery.merger import Merger

        Merger().run(dry_run=not args.delete)
    elif args.scan is not None:
        from mgallery.scanner import Scanner

        Scanner(args.scan).run()
    else:
        parser.print_help()
