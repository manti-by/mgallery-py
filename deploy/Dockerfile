# Use an official python 3.7 image
FROM python:3.7


# Update base image
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y supervisor && \
    apt-get autoremove --purge && \
    apt-get clean


# Create required dirs
RUN mkdir -p /srv/mgallery/ && \
    mkdir -p /etc/mgallery/ && \
    mkdir -p /var/log/mgallery/ && \
    mkdir -p /var/lib/mgallery/


# Set working directory and expose ports
WORKDIR /srv/mgallery/
RUN git init && \
    git remote add origin https://github.com/manti-by/mgallery.git && \
    git pull origin master


# Install Dokerize plugin
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz && \
    tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz && \
    rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz


# Install app requirements
COPY requirements.txt /etc/mgallery/requirements.txt
RUN pip install --trusted-host pypi.org --no-cache-dir --upgrade pip && \
    pip install --trusted-host pypi.org --no-cache-dir -r /etc/mgallery/requirements.txt


# Fix file permissions
RUN chown -R www-data:www-data /srv/mgallery/ && \
    chown -R www-data:www-data /etc/mgallery/ && \
    chown -R www-data:www-data /var/log/mgallery/ && \
    chown -R www-data:www-data /var/lib/mgallery/


# Setup supervisor
COPY supervisor.conf /etc/supervisor/conf.d/mgallery.conf
CMD supervisord -n -c /etc/supervisor/supervisord.conf