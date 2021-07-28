FROM python:3.8-slim-buster

ENV PYTHONBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y \
    # Simple init script
    dumb-init \
    # duh
    make \
    # helpful packages. curl to curl and jq to make it pretty
    jq curl \
    && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY conf/web/requirements.txt /code/conf/web/requirements.txt

RUN pip install -r /code/conf/web/requirements.txt

CMD ["/bin/bash"]

# COPY ny_data /opt/code/ny_data
# COPY src /opt/code/src
# COPY app.py /opt/code/app.py

COPY . /code/
