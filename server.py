import yaml
from aiohttp import web, ClientSession, TCPConnector
import async_timeout


def get_config() -> dict:
    with open('config.yml') as f:
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
    return web.Response(text='Hello!')

async def metrics(request):
    result = '# HELP probe_success Displays whether or not the probe was a success\n'
    result += '# TYPE probe_success gauge\n'

    config = get_config()
    for target in config.get('targets', []):
        probe_success = await is_probe_success(target=target)
        result += 'probe_success{target="%s",name="%s"} %s\n' % (target['url'], target['name'], int(probe_success))

    return web.Response(text=result)


app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/metrics', metrics)
web.run_app(app, host='0.0.0.0', port=9115)
