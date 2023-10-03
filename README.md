Image deduplication app
====


About
----

Image deduplicate script and GTK app to compare.

[![Python 3.11](https://img.shields.io/badge/python-3.11-green.svg)](https://www.python.org/downloads/release/python-3111/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/manti-by/mgallery/master/LICENSE)

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://github.com/manti-by/mgallery-py/

Rust mirror: https://github.com/manti-by/mgallery-rust/

Requirements:

    Python 3.11, OpenCV, Redis, GTK


Script setup
----

1. Create virtualenv and install packages from requirements file.

2. Install libraw and set appropriate environment variables:

   ```bash
   sudo apt install libraw-dev
   
   export REDIS_URL=redis://127.0.0.1:6379/5
   export GALLERY_PATH=/home/ubuntu/app/data/
   ```

3. Scan gallery and compare duplicates

   ```bash
   make setup
   make scan
   make compare
   ```
