import click
from aiohttp import web
from hashlib import sha256



@click.command()
@click.option('--host', default='127.0.0.1', help='Хост сервера')
@click.option('--port', default=8080, help='Порт сервера')
def run_server(host: str, port: int) -> web.Application:
    """
        Запуск сервера
        С помощью библиотек Click получаем хост и порт для запуска сервера

        args:
            host - строка задающая хост для запуска сервера
            port - порт для запуска сервера
        
        return:
            None
    """

    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_post('/hash', hash)

    web.run_app(app)
    return app


async def healthcheck(request: web.Request) -> web.Response:
    """
        Обработчик GET-запроса к /healthcheck
        Возвращает пустой статус код -200 и пустой json

        args:
            request - web.Request object

        return:
            web.Response
    """

    return web.json_response(status=200, data={})


async def get_hash_string(string: str) -> str:
    """
        Создаёт хэш переданной строки

        args:
            string - строка для высчитывания хэша

        return:
            str
    """

    return sha256(string.encode('utf-8')).hexdigest()


async def hash(request: web.Request) -> web.Response:
    """
        Обработчик POST-запроса к /hash
        Проверяет, что в теле запроса есть ключ string
        и возвращает вычисленный хэш строки

        args:
            request - web.Request object

        return:
            web.Response
    """

    data = await request.json()
    string = data.get('string')
    if string is not None:
        hash_string = await get_hash_string(string)
        json_data = {"hash_string": hash_string}
        status = 200
    else:
        status = 400
        json_data = {"validation_errors": "string field not found in json"}

    return web.json_response(status=status, data=json_data)

if __name__ == '__main__':
    app = run_server()
