Gallery with face recognition
====


About
----

Custom gallery engine.

[![CircleCI](https://img.shields.io/circleci/project/github/manti-by/MGallery/master.svg)](https://circleci.com/gh/manti-by/mgallery)
[![Docker](https://img.shields.io/docker/automated/mantiby/mgallery.svg)](https://hub.docker.com/r/mantiby/mgallery/)

[![Python 3.7](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-370/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/manti-by/mgallery/master/LICENSE)

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://github.com/manti-by/MGallery/

Requirements:

    Python 3.7, PostgreSQL, Redis, Celery


Docker setup
----

1. Install [Docker](https://docs.docker.com/install/) and 
[docker-compose](https://docs.docker.com/compose/install/)

2. Build app image and run

        $ make build
        $ make local

3. Scan gallery and merge duplicates

        $ make scan
        $ make merge


NOTE: For additional commands check Makefile
