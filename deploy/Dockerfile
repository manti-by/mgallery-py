# Use an official python 3.6 image

FROM python:3.6


# Create required dirs

RUN mkdir -p /srv/mgallery/
RUN mkdir -p /etc/mgallery/
RUN mkdir -p /var/run/mgallery/
RUN mkdir -p /var/log/mgallery/


# Install any needed packages

RUN apt-get update && apt-get install -y cmake supervisor
RUN apt-get clean

COPY requirements.txt /etc/mgallery/requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.org --no-cache-dir -r /etc/mgallery/requirements.txt


# Install Dockerize

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz


# Setup supervisor

COPY supervisor.conf /etc/supervisor/conf.d/mgallery.conf


# Set working directory and expose ports

WORKDIR /srv/mgallery/app/
RUN git init
RUN git remote add origin https://github.com/manti-by/mgallery.git


# Fix file permissions

RUN chown -R www-data:www-data /srv/mgallery/
RUN chown -R www-data:www-data /run/mgallery/
RUN chown -R www-data:www-data /var/log/mgallery/
RUN chown -R www-data:www-data /var/run/


# Start app services

CMD supervisord -n -c /etc/supervisor/supervisord.conf