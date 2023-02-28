#!/usr/bin/env python
import argparse

import logging.config

from mgallery.settings import LOGGING

logging.config.dictConfig(LOGGING)

parser = argparse.ArgumentParser(
    prog="python mgallery.py", description="Image deduplicate script.", add_help=True
)

parser.add_argument(
    "-s",
    "--scan",
    action="store_true",
    default=False,
    help="Scan directory for images",
)
parser.add_argument(
    "-c",
    "--compare",
    action="store_true",
    default=False,
    help="Compare duplicated images",
)
parser.add_argument(
    "-r",
    "--resort",
    action="store_true",
    default=False,
    help="Resort/rename images in the current directory",
)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.scan:
        from mgallery.scanner import run_scanner

        run_scanner()
    elif args.compare:
        from mgallery.compare import run_compare

        run_compare()
    elif args.resort:
        from mgallery.resort import run_resort

        run_resort()
    else:
        parser.print_help()
