import asyncio
import csv
from typing import Optional, TypedDict

from aiomysql import Pool

from db import create_connect_db
from utils import CryptoGuard, read_config


class StaffUser(TypedDict):
    id: int
    employee_name: str
    login: str
    password: Optional[str]
    unhashed_password: Optional[str]
    can_login: str

async def get_user_without_password(db: Pool):
    query = """
SELECT
    s.id
    , s.employee_name
    , s.login
    , s.password
    , s.can_login
FROM
    staff s
WHERE
    s.password IS NULL
    AND s.can_login IS TRUE
    """
    users: list[StaffUser] = []
    async with db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
            users = await cur.fetchall()
    return users

async def generate_passwords(cg: CryptoGuard, staff: list[StaffUser]):
    for user in staff:
        unhashed_password = cg.generate_password()
        password = cg.hash_password(unhashed_password)
        user["password"] = password
        user["unhashed_password"] = unhashed_password
    return staff

def create_csv(staff: list[StaffUser]):
    keys = [
            "id",
            "employee_name",
            "login",
            "password",
            "unhashed_password",
            "can_login"
            ]
    with open("staff_pass.csv", "w", encoding="utf-8") as f:
        w = csv.DictWriter(f, keys, delimiter=";")
        w.writeheader()
        w.writerows(staff)

async def main():
    cnf = read_config("config.toml")
    cg = CryptoGuard(cnf["service"]["secret"])
    db = await create_connect_db(**cnf["database"])
    staff = await get_user_without_password(db)
    await generate_passwords(cg, staff)
    create_csv(staff)
    db.close()
    await db.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
