Gallery with face recognition
====


About
----

Image deduplicate script.

[![Python 3.9](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-370/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/manti-by/mgallery/master/LICENSE)

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://github.com/manti-by/mgallery/

Requirements:

    Python 3.9, Redis, ImageHash, Pillow


Script setup
----

1. Create virtualenv and install packages from requirements file.

2. Set appropriate environment variables:

        GALLERY_PATH=/home/ubuntu/mgallery/photo/
        DATABASE_PATH=/home/ubuntu/mgallery/db.sqlite
        REDIS_URL=redis://localhost:6379/0
        DEBUG_LOG=/home/ubuntu/mgallery/debug.log
        ERROR_LOG=/home/ubuntu/mgallery/error.log

3. Scan gallery and merge duplicates

        $ make scan
        $ make merge


NOTE: For additional commands check Makefile
