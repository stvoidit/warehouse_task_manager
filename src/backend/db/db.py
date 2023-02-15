# pylint: disable=too-many-lines

from aiomysql import Connection


async def select_tasks(conn: Connection, user_id: int, stock_id: int):
    """ получение списка заданий """
    q = """
SELECT
    m.material
    , m.id AS material_id
    , doc.id AS doc_id
    , doc.doc_number
    , doc.planned_date
    , doc.technical_process
    , doc.operation
    , tare_type
    , SUM(tare_amount) AS amount
    , SUM(net_weight) AS weight
    , SUM(tare_amount_fact) AS amount_fact
    , SUM(net_weight_fact) AS weight_fact
FROM
    production_task
LEFT JOIN production_task_doc AS doc ON
    doc.id = production_task.doc_id
LEFT JOIN material AS m ON
    m.id = production_task.material
INNER JOIN (
        SELECT
            tare_type
            , key_material
        FROM
            arrival
        LEFT JOIN arrival_doc ON
            arrival_doc.id = arrival.doc_id
        WHERE
            arrival_doc.stock = %(stock_id)s
    ) AS A ON
    A.key_material = production_task.key_material
WHERE
    doc.id IN (
        SELECT
            production_task_executor.doc_id
        FROM
            production_task_executor
        WHERE
            production_task_executor.executor_id = %(user_id)s
    )
    AND
    doc.done = 0
GROUP BY
    m.material
    , m.id
    , doc.id
    , doc.doc_number
    , doc.planned_date
    , doc.technical_process
    , doc.operation
    , tare_type
ORDER BY
    doc.id ASC
    , m.id ASC
    """
    result = []
    async with conn.cursor() as cur:
        await cur.execute(q, { "user_id": user_id, "stock_id": stock_id })
        result = await cur.fetchall()
    return result


async def select_task_meta(conn: Connection, stock_id: int, doc_id: int):
    q = """
SELECT
    ptd.id
    , ptd.doc_number
    , ptd.doc_date
    , ptd.planned_date
    , ptd.stock
    , ptd.technical_process
    , ptd.operation
    , task.material
FROM
    production_task_doc ptd
LEFT JOIN (
        SELECT
            DISTINCT
            pt.doc_id
            , m.material
        FROM
            production_task pt
        INNER JOIN material AS m ON
            m.id = pt.material
    ) AS task ON
    task.doc_id = ptd.id
WHERE
    ptd.id = %(doc_id)s
    AND
    ptd.stock = %(stock_id)s
    AND
    ptd.done = 0
    """
    task = None
    async with conn.cursor() as cur:
        await cur.execute(q, {"doc_id": doc_id, "stock_id": stock_id})
        task = await cur.fetchone()
    return task

async def select_task(conn: Connection, stock_id: int, doc_id: int, material_id: int):
    """ получение позиций задания """
    q = """
SELECT
    m.material
    , arrival.material
    , arrival.tare_id
    , arrival.tare_mark
    , arrival.tare_type
    , arrival.tare_amount - IFNULL(P.tare_amount, 0) - IFNULL(S.tare_amount, 0) AS rest_tare_amount
    , arrival.net_weight - IFNULL(P.net_weight, 0) - IFNULL(S.net_weight, 0) + IFNULL(tare.weight, 0) * (arrival.tare_amount - IFNULL(P.tare_amount, 0) - IFNULL(S.tare_amount, 0)) AS rest_gross_weight
    , task.tare_amount AS task_tare_amount
    , task.net_weight AS task_net_weight
    , task.done
FROM
    arrival
LEFT JOIN (
        SELECT
            *
        FROM
            production
        LEFT JOIN production_doc ON
            production_doc.id = production.doc_id
        WHERE
            production_doc.stock = %(stock)s
    ) P ON
    P.key_material = arrival.key_material
LEFT JOIN (
        SELECT
            *
        FROM
            shipment
        LEFT JOIN shipment_doc ON
            shipment_doc.id = shipment.doc_id
        WHERE
            shipment_doc.stock = %(stock)s
    ) S ON
    S.key_material = arrival.key_material
LEFT JOIN material AS m ON
    m.id = arrival.material
LEFT JOIN tare ON
    arrival.tare_type = tare.id
LEFT JOIN (
        SELECT
            lab.key_material
            , TRIM(GROUP_CONCAT(lab.material_mark SEPARATOR ' ')) AS lab_material_mark
            , TRIM(GROUP_CONCAT(lab.material_group SEPARATOR ' ')) AS lab_material_group
        FROM
            laboratory AS lab
        GROUP BY
            lab.key_material
    ) L ON
    L.key_material = arrival.key_material
LEFT JOIN arrival_doc ON
    arrival_doc.id = arrival.doc_id
INNER JOIN (
        SELECT
            key_material
            , tare_amount
            , net_weight
            , tare_amount_fact
            , net_weight_fact
            , production_task.done
        FROM
            production_task
        LEFT JOIN production_task_doc ON
            production_task_doc.id = production_task.doc_id
        WHERE
            production_task_doc.id = %(doc_id)s
            AND production_task_doc.stock = %(stock)s
    ) AS task ON
    task.key_material = arrival.key_material
WHERE
    arrival_doc.stock = %(stock)s
    AND
    m.id = %(material_id)s
ORDER BY
    m.material
    , arrival.tare_id
    """
    task = await select_task_meta(conn, stock_id, doc_id)
    if task is None:
        return task
    jobs = []
    async with conn.cursor() as cur:
        await cur.execute(q, {"doc_id": doc_id, "stock": stock_id, "material_id": material_id})
        jobs = await cur.fetchall()
    task["jobs"] = jobs
    return task


async def check_user(conn: Connection, login: str, password_hash: str):
    """ проверка авторизации пользователя """
    q = """
SELECT
    s.id
    , s.login
    , s.employee_name
    , s.can_login
FROM
    staff s
WHERE
    s.can_login IS TRUE
    AND
    s.login = %(login)s
    AND
    s.password = %(password_hash)s
    """
    result = {}
    async with conn.cursor() as cur:
        await cur.execute(q, {"login": login, "password_hash": password_hash})
        result = await cur.fetchone()
    return result

async def change_password(conn: Connection, user_id: int, password_hash: str):
    q = """
    UPDATE staff
    SET password=%(password_hash)s
    WHERE id = %(user_id)s AND can_login = 1
    """
    async with conn.cursor() as cur:
        await cur.execute(q, {"user_id": user_id, "password_hash": password_hash})

async def check_can_login(conn: Connection, user_id: int):
    """ проверка возможности входа по токену"""
    q = """ SELECT EXISTS (SELECT TRUE FROM staff s WHERE s.id = %(user_id)s AND s.can_login IS TRUE ) AS can_login """
    can_login = False
    async with conn.cursor() as cur:
        await cur.execute(q, {"user_id": user_id})
        result = await cur.fetchone()
        if result.get("can_login", 0) == 1:
            can_login = True
    return can_login

async def select_stocks(conn: Connection, user_id: int):
    q = """
SELECT
    s.id
    , s.name
    , SUM(IF(ptd.done = 0 AND pte.executor_id = %(user_id)s, 1, 0)) tasks_count
FROM
    stock s
LEFT JOIN production_task_doc ptd ON
    ptd.stock = s.id
LEFT JOIN production_task_executor pte ON
    pte.doc_id = ptd.id
GROUP BY
    s.id
    , s.name
ORDER BY
    s.name
    """
    stocks = []
    async with conn.cursor() as cur:
        await cur.execute(q, {"user_id": user_id})
        stocks = await cur.fetchall()
    return stocks

async def update_job_status(conn: Connection, doc_id: int, user_id: int, material_id: int, tara_id: int, status: bool):
    q = """
UPDATE
    production_task
SET
    done = %(status)s
    , net_weight_fact = CASE WHEN %(status)s IS TRUE THEN net_weight ELSE net_weight_fact = 0 END
    , tare_amount_fact = CASE WHEN %(status)s IS TRUE THEN tare_amount ELSE tare_amount_fact = 0 END
    , fact_executor = CASE WHEN %(status)s IS TRUE THEN %(user_id)s ELSE fact_executor = 0 END
WHERE
    material = %(material_id)s
    AND
    doc_id = %(doc_id)s
    AND
    tare_id = %(tara_id)s
    """
    async with conn.cursor() as cur:
        await cur.execute(q, {"doc_id": doc_id, "user_id": user_id, "material_id": material_id, "tara_id": tara_id, "status": status})
    return
