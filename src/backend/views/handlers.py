from aiohttp.web import Request, HTTPBadRequest, HTTPForbidden

from db import (
    select_tasks,
    select_task,
    check_user)
from utils import jsonify


async def login_handler(request: Request):
    body = await request.json()
    login = body.get("login", "")
    security = request.app["crypto"]
    password_hash = security.hash_password(body.get("password", ""))
    user = None
    async with request.app["db"].acquire() as conn:
        user = await check_user(conn, login, password_hash)
    if user is None:
        raise HTTPForbidden()
    return await jsonify(security.create_jwt(user), request)


async def get_tasks(request: Request):
    user_id = 2
    tasks = []
    async with request.app["db"].acquire() as conn:
        tasks = await select_tasks(conn, user_id)
    return await jsonify(tasks, request)


async def get_task(request: Request):
    doc_id = request.match_info.get("taskID", None)
    if doc_id is None:
        raise HTTPBadRequest()
    task_positions = []
    async with request.app["db"].acquire() as conn:
        task_positions = await select_task(conn, doc_id)
    return await jsonify(task_positions, request)
