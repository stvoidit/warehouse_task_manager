from aiohttp.web import HTTPBadRequest, HTTPForbidden, HTTPCreated, Request

from db import check_user, select_task, select_tasks, change_password
from utils import jsonify


async def login_handler(request: Request):
    """ хэндлен авторизация """
    security = request.app["crypto"]
    body = await request.json()
    login = body.get("login", "")
    password = body.get("password", "")
    password_hash = security.hash_password(password)
    user = None
    async with request.app["db"].acquire() as conn:
        user = await check_user(conn, login, password_hash)
    if user is None:
        raise HTTPForbidden()
    return await jsonify(security.create_jwt(user), request)


async def change_password_handler(request: Request):
    """ хэндер смены пароля """
    security = request.app["crypto"]
    body = await request.json()
    new_password = body.get("newPassword")
    repetition_password = body.get("repetitionPassword")
    if new_password is None or repetition_password is None or new_password != repetition_password:
        raise HTTPBadRequest(body="Проверьте корректность запроса")
    password_hash = security.hash_password(new_password)
    async with request.app["db"].acquire() as conn:
        await change_password(conn, request.user_id, password_hash)
    return HTTPCreated()

async def get_tasks(request: Request):
    """ получение списка заданий """
    tasks = []
    async with request.app["db"].acquire() as conn:
        tasks = await select_tasks(conn, request.user_id)
    return await jsonify(tasks, request)


async def get_task(request: Request):
    """ получение позиций в задании """
    # TODO: нужна привязка еще и по ID юзера
    doc_id = request.match_info.get("taskID", None)
    if doc_id is None:
        raise HTTPBadRequest()
    task = {}
    async with request.app["db"].acquire() as conn:
        task = await select_task(conn, doc_id)
    return await jsonify(task, request)
