FROM vinta/python:2.7.apt

MAINTAINER Vinta Chen <vinta.chen@gmail.com>

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libyaml-dev \
    zlib1g-dev && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
COPY requirements_test.txt /app/
RUN pip install -r requirements_test.txt

CMD ["pip", "list"]
