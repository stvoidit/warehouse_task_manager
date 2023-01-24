import logging

from aiohttp import web
from uvloop import install as uvinstall

from db import create_connect_db
from middlewares import middleware_check_token, middleware_compression
from utils import CryptoGuard, read_config
from views import setup_handlers

uvinstall()


async def _on_shutdown(app: web.Application):
    """ мягкое завершение работы - отключение от БД """
    print("shutdown")
    app["db"].close()
    await app["db"].wait_closed()


async def _on_startup(app: web.Application):
    """ инициализация соединения с БД """
    app["db"] = await create_connect_db(**app["config"]["database"])

async def init_app() -> web.Application:
    """ инициализация всего приложения """
    logging.basicConfig(level=logging.INFO)
    app = web.Application(middlewares=[ middleware_check_token, middleware_compression ])
    cnf = read_config("config.toml")
    app["config"] = cnf
    app["crypto"] = CryptoGuard(cnf["service"]["secret"])
    app.on_startup.append(_on_startup)
    app.on_shutdown.append(_on_shutdown)
    await setup_handlers(app)
    return app


if __name__ == "__main__":
    web.run_app(app=init_app(), host="0.0.0.0", port=8080)
