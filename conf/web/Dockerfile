FROM python:3.8-slim-buster

WORKDIR /opt/code
ENV PYTHONPATH=/opt/code/src

RUN apt-get update && apt-get install -y \
    # dev library for talking to mysql
    default-libmysqlclient-dev \
    # Simple init script
    dumb-init \
    # duh
    make \
    # helpful packages. curl to curl and jq to make it pretty
    jq curl \
    && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY conf/web/requirements.txt /opt/code/conf/web/requirements.txt

RUN apt-get update && pip install -r /opt/code/conf/web/requirements.txt

CMD ["/bin/bash"]

COPY src /opt/code/src

#run app.py with python
#CMD ["python","src/app.py"]
