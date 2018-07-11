Gallery scanner with AI features
====


About
----

Custom gallery engine with AI features.

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://bitbucket.org/manti_by/mgallery/

Requirements:

    Python 3+, PostgreSQL


Docker setup
----

1. Install [Docker](https://docs.docker.com/install/) and 
[docker-compose](https://docs.docker.com/compose/install/)

2. Build app image and run

        $ cd deploy/ 
        $ docker build -f Dockerfile -t mantiby/mgallery:latest .
        $ docker-compose up
