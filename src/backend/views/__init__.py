import pathlib
from aiohttp.web import Application, Request, FileResponse

from .handlers import (
    get_tasks,
    get_task
)


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
        ("GET", "/api/tasks", get_tasks, "get_tasks"),
        ("GET", "/api/task/{taskID}", get_task, "get_task")
    ]
    for method, path, func, name in [*views]:
        app.router.add_route(method, path, func, name=name)
