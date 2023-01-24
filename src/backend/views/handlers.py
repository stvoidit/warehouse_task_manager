from aiohttp.web import Request, HTTPBadRequest

from db import (select_tasks, select_task)
from utils import jsonify


async def login(request: Request):
    pass

async def logout(request: Request):
    pass


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
