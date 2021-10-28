#!/usr/bin/env python
import argparse
import asyncio

from mgallery.logger import setup_logger
from mgallery.report import generate_report
from mgallery.scanner import run_scanner

parser = argparse.ArgumentParser(
    prog="python mgallery.py", description="Image deduplicate script.", add_help=True
)

parser.add_argument(
    "-s",
    "--scan",
    action="store_true",
    default=True,
    help="Scan directory for images",
)
parser.add_argument(
    "-r",
    "--report",
    action="store_true",
    default=False,
    help="Generate report for duplicated images",
)
parser.add_argument(
    "-v", "--verbose", action="count", default=0, help="Increase output verbosity"
)


if __name__ == "__main__":
    args = parser.parse_args()
    setup_logger(args.verbose)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if args.report:
        loop.run_until_complete(generate_report())
    elif args.scan:
        loop.run_until_complete(run_scanner())
    else:
        parser.print_help()
