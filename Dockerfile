FROM python:3.9

COPY . /opt/app
WORKDIR /opt/app
RUN pip3 install -r requirements.txt


EXPOSE 9115
ENV PYTHONUNBUFFERED 1

ENTRYPOINT python3.9 server.py
