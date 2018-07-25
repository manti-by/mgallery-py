# Use an official python 3.6 image

FROM python:3.6


# Create required dirs

RUN mkdir -p /srv/mgallery/
RUN mkdir -p /etc/mgallery/
RUN mkdir -p /run/mgallery/
RUN mkdir -p /var/log/mgallery/


# Install any needed packages

RUN apt-get update && apt-get install -y cmake supervisor
RUN apt-get clean

COPY requirements.txt /etc/mgallery/requirements.txt
RUN pip3 install --trusted-host pypi.org --no-cache-dir -r /etc/mgallery/requirements.txt


# Setup supervisor

COPY supervisor.conf /etc/mgallery/supervisor.conf
RUN ln -s /etc/mgallery/supervisor.conf /etc/supervisor/conf.d/mgallery.conf


# Set working directory and expose ports

WORKDIR /srv/mgallery/app/


# Fix file permissions

RUN chown -R www-data:www-data /srv/mgallery/
RUN chown -R www-data:www-data /run/mgallery/
RUN chown -R www-data:www-data /var/log/mgallery/


# Start app services

CMD supervisord -n