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
docker run -it --rm -v /<full_path_to_config>/config.yml:/opt/app/config.yml -p 9115:9115 telminov/prometheus-http-exporter

```

run container detached
```bash
docker run -d --name http_exporter -v /<full_path_to_config>/config.yml:/opt/app/config.yml -p 9115:9115 telminov/prometheus-http-exporter

```
