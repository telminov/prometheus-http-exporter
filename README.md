[![Build Status](https://travis-ci.org/telminov/prometheus-http-exporter.svg?branch=master)](https://travis-ci.org/telminov/prometheus-http-exporter)

# prometheus-http-exporter
Prometheus http service status exporter

## docker
build image
```bash
docker build -t prometheus-http-exporter .
```
or get image
```bash
docker pull telminov/prometheus-http-exporter
```

run container interactive
```bash
docker run -it --rm -v .../config.yml:/opt/app/config.yml -p 9115:9115 telminov/prometheus-http-exporter
```

run container detached
```bash
docker run -d --name http_exporter -v .../config.yml:/opt/app/config.yml -p 9115:9115 telminov/prometheus-http-exporter
```
