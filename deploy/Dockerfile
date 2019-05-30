# Use an official python 3.7 image
FROM python:3.7-slim


# Update base image
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wget supervisor && \
    apt-get autoremove --purge && \
    apt-get clean


# Create required dirs
RUN mkdir -p /srv/mgallery/ && \
    mkdir -p /etc/mgallery/ && \
    mkdir -p /var/log/mgallery/ && \
    mkdir -p /var/lib/mgallery/


# Install app requirements
COPY requirements.txt /etc/mgallery/requirements.txt
RUN pip install --trusted-host pypi.org --no-cache-dir --upgrade pip && \
    pip install --trusted-host pypi.org --no-cache-dir -r /etc/mgallery/requirements.txt


# Fix file permissions for celery worker
RUN chown -R www-data:www-data /srv/mgallery/ && \
    chown -R www-data:www-data /etc/mgallery/ && \
    chown -R www-data:www-data /var/log/mgallery/ && \
    chown -R www-data:www-data /var/lib/mgallery/


# Setup supervisor
WORKDIR /srv/mgallery/app/
COPY supervisor.conf /etc/supervisor/conf.d/mgallery.conf
CMD supervisord -n -c /etc/supervisor/supervisord.conf
