Gallery with face recognition
====


About
----

Image deduplicate script.

[![Python 3.9](https://img.shields.io/badge/python-3.9-green.svg)](https://www.python.org/downloads/release/python-370/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/manti-by/mgallery/master/LICENSE)

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://github.com/manti-by/mgallery-py/

Rust mirror: https://github.com/manti-by/mgallery-rust/

Requirements:

    Python 3.9, ImageHash, Pillow


Script setup
----

1. Create virtualenv and install packages from requirements file.

2. Set appropriate environment variables:

        GALLERY_PATH=/home/ubuntu/mgallery/data/
        DATABASE_PATH=/home/ubuntu/mgallery/db.sqlite
        DEBUG_LOG=/home/ubuntu/mgallery/logs/debug.log
        ERROR_LOG=/home/ubuntu/mgallery/logs/error.log

3. Scan gallery and compare duplicates

        $ make scan
        $ make compare


NOTE: For additional commands check Makefile
