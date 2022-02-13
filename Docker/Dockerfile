FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get -y install --no-install-recommends python3-pip && \
    useradd -r -m -u 1000 urtc

COPY app /home/urtc/app

WORKDIR /home/urtc

RUN pip3 install -r app/requirements.txt && \
    chmod +x app/app.py && \
    chown -R urtc: .
