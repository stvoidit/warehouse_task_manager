from multiprocessing import cpu_count
from os import getenv

from aiomysql import DictCursor, Pool, create_pool

from .db import check_user, select_task, select_tasks, change_password, select_stocks


async def create_connect_db(user: str, password: str, host: str, port: int, db: str) -> Pool:
    return await create_pool(
        user=user,
        password=password,
        host=host,
        port=port,
        db=db,
        minsize=0,
        maxsize=cpu_count()*10,
        autocommit=True,
        cursorclass=DictCursor
    )


__all__ = (
    "select_tasks",
    "select_task",
    "check_user",
    "change_password",
    "select_stocks",
)
