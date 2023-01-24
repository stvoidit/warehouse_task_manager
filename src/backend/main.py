import logging

from aiohttp import web
from uvloop import install as uvinstall

from db import create_connect_db
from views import setup_handlers
from utils import read_config, CyptoPassword

from middlewares import middleware_check_token
uvinstall()


async def _on_shutdown(app: web.Application):
    print("shutdown")
    app["db"].close()
    await app["db"].wait_closed()


async def _on_startup(app: web.Application):
    app["db"] = await create_connect_db(**app["config"]["database"])

async def init_app() -> web.Application:
    # middlewares=[middleware1]
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    cnf = read_config("config.toml")
    app["config"] = cnf
    app["crypto"] = CyptoPassword(cnf["service"]["secret"])
    app.middlewares.append(middleware_check_token)
    app.on_startup.append(_on_startup)
    app.on_shutdown.append(_on_shutdown)
    await setup_handlers(app)
    return app


if __name__ == "__main__":
    web.run_app(app=init_app(), host="0.0.0.0", port=8080)
