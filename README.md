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

    Python 3.9, ImageHash, Pillow


Script setup
----

1. Create virtualenv and install packages from requirements file.

2. Set appropriate environment variables:

        GALLERY_PATH=/home/ubuntu/mgallery/photo/
        DATABASE_PATH=/home/ubuntu/mgallery/db.sqlite
        DEBUG_LOG=/home/ubuntu/mgallery/debug.log
        ERROR_LOG=/home/ubuntu/mgallery/error.log

3. Install system libraries (for GUI app)

        $ sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
        $ sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev

4. Setup environment and install packages from requirements file:

        $ pip3 install -r requirements.txt

5. Scan gallery and merge duplicates

        $ make scan
        $ make merge


NOTE: For additional commands check Makefile
