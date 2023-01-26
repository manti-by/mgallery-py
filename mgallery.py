#!/usr/bin/env python
import argparse
import asyncio
import sqlite3

from mgallery.compare import run_compare
from mgallery.logger import setup_logger
from mgallery.report import generate_report
from mgallery.scanner import run_scanner
from mgallery.settings import DATABASE_PATH

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
    "-r",
    "--report",
    action="store_true",
    default=False,
    help="Generate report for duplicated images",
)
parser.add_argument(
    "-c",
    "--compare",
    action="store_true",
    default=False,
    help="Compare duplicated images",
)
parser.add_argument(
    "-v", "--verbose", action="count", default=0, help="Increase output verbosity"
)


if __name__ == "__main__":
    args = parser.parse_args()
    setup_logger(args.verbose)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    session = sqlite3.connect(DATABASE_PATH)

    if args.report:
        loop.run_until_complete(generate_report(session))
    elif args.scan:
        loop.run_until_complete(run_scanner(session))
    elif args.compare:
        loop.run_until_complete(run_compare(session))
    else:
        parser.print_help()
