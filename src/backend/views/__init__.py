import pathlib

from aiohttp.web import Application, FileResponse, Request

from .handlers import get_task, get_tasks, login_handler, change_password_handler

def index_spa(path, filename):
    static_files = [p.name for p in pathlib.Path(path).iterdir() if p.is_dir() is False]
    async def static_view(request: Request):
        path_to_file = pathlib.Path(path, filename)
        if request.path.removeprefix("/") in static_files:
            path_to_file = pathlib.Path(path, request.path.removeprefix("/"))
        return FileResponse(path_to_file)
    return static_view


async def setup_handlers(app: Application):
    try:
        app.router.add_static("/assets", "static/assets")
        app.router.add_get("/{path:(?!api).*}", index_spa("static", "index.html"))
    except ValueError:
        print("static dir not found")

    views = [
        ("POST", "/api/login", login_handler, "login"),
        ("POST", "/api/change_password", change_password_handler, "change_password"),
        ("GET", "/api/tasks", get_tasks, "get_tasks"),
        ("GET", "/api/task/{taskID}", get_task, "get_task")
    ]
    for method, path, func, name in [*views]:
        app.router.add_route(method, path, func, name=name)
