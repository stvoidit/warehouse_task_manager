import pathlib

from aiohttp.web import Application, FileResponse, Request

from .handlers import (
    change_password_handler, get_stocks, get_task,
    get_tasks, login_handler, tasks_progress,
    update_job_status_handler, rest_gross_weight
)


def index_spa(path: str, filename: str):
    static_files = [p.name for p in pathlib.Path(
        path).iterdir() if p.is_dir() is False]

    async def static_view(request: Request):
        path_to_file = pathlib.Path(path, filename)
        if request.path.removeprefix("/") in static_files:
            path_to_file = pathlib.Path(path, request.path.removeprefix("/"))
        return FileResponse(path_to_file)
    return static_view


def setup_handlers(app: Application):
    try:
        app.router.add_static("/assets", "static/assets")
        app.router.add_get("/{path:(?!api).*}",
                           index_spa("static", "index.html"))
    except ValueError:
        print("static dir not found")

    views = [
        ("POST", "/api/login", login_handler, "login"),
        ("POST", "/api/change_password", change_password_handler, "change_password"),
        ("PUT", "/api/job", update_job_status_handler, "update_job_status"),
        ("GET", "/api/stocks", get_stocks, "get_stocks"),
        ("GET", "/api/stock/{stockID}/tasks", get_tasks, "get_tasks"),
        ("GET", "/api/stock/{stockID}/tasks_progress",
         tasks_progress, "tasks_progress"),
        ("GET", "/api/stock/{stockID}/task/{taskID}/material/{materialID}",
         get_task, "get_task"),
        ("PUT", "/api/rest_gross_weight", rest_gross_weight, "rest_gross_weight")
    ]
    for method, path, func, name in [*views]:
        app.router.add_route(method, path, func, name=name)
