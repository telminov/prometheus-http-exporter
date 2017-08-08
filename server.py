#! /usr/bin/env python
import argparse
import yaml
from aiohttp import web, ClientSession, TCPConnector
import async_timeout

parser = argparse.ArgumentParser(description='Prometheus HTTP exporter.')
parser.add_argument('-c', '--config', dest='config', default='config.yml',
                    help='Path to configuration yaml-file. Default config.yml')
parser.add_argument('--host', dest='host', default='0.0.0.0',
                    help='HTTP server host. Default 0.0.0.0')
parser.add_argument('-p', '--port', dest='port', default=9115, type=int,
                    help='HTTP server port. Default 9115')
args = parser.parse_args()


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/metrics', metrics)
    return app


def get_config() -> dict:
    config_path = args.config
    with open(config_path) as f:
        config_data = yaml.load(f)
    return config_data


async def is_probe_success(target: dict) -> bool:
    try:
        url = target['url']
        verify_ssl = target.get('verify_ssl', True)

        connector = TCPConnector(verify_ssl=verify_ssl)
        async with ClientSession(connector=connector) as session:
            with async_timeout.timeout(10):
                async with session.get(url) as response:
                    return response.status < 400
    except Exception as ex:
        print(ex)
        return False

async def index(request):
    return web.Response(text='<h1>HTTP exporter</h1><p><a href="/metrics">Metrics</a><p>', content_type='text/html')

async def metrics(request):
    result = '# HELP probe_success Displays whether or not the probe was a success\n'
    result += '# TYPE probe_success gauge\n'

    config = get_config()
    for target in config.get('targets', []):
        probe_success = await is_probe_success(target=target)
        result += 'probe_success{target="%s",name="%s"} %s\n' % (target['url'], target['name'], int(probe_success))

    return web.Response(text=result)


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host=args.host, port=args.port)
