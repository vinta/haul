FROM python:2.7.9

MAINTAINER Vinta Chen <vinta.chen@gmail.com>

RUN apt-get update && \
    apt-get install -y \
    libxml2-dev \
    libxslt1-dev && \
    apt-get clean && \
    apt-get purge && \
    apt-get autoremove -y && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN mkdir -p /app
WORKDIR /app

# COPY requirements.txt /app/
# COPY requirements_test.txt /app/
# RUN pip install -r requirements_test.txt

# CMD ["/run.sh"]
