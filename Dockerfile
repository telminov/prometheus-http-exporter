FROM python:3.6

RUN pip3 install aiohttp==2.2.5 \
        pyyaml==3.12

COPY . /opt/app
WORKDIR /opt/app

EXPOSE 9115
VOLUME /conf/
ENV PYTHONUNBUFFERED 1

ENTRYPOINT python3.6 server.py
