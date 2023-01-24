# pylint: disable=too-many-lines

from aiomysql import Connection


async def select_tasks(conn: Connection, user_id: int):
    """ получение списка заданий """
    q = """
SELECT
    m.material
    , doc.id AS doc_id
    , doc.doc_number
    , doc.planned_date
    , doc.technical_process
    , doc.operation
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
WHERE
    doc.id IN
(
        SELECT
            production_task_executor.doc_id
        FROM
            production_task_executor
        LEFT JOIN staff ON
            staff.id = production_task_executor.executor_id
        WHERE
            staff.id = %(user_id)s
    )
GROUP BY
    m.material
    , doc.id
    , doc.doc_number
    , doc.planned_date
    , doc.technical_process
    , doc.operation
    """
    result = []
    async with conn.cursor() as cur:
        await cur.execute(q, {"user_id": user_id})
        result = await cur.fetchall()
    return result


async def select_task(conn: Connection, doc_id: int):
    """ получение позиций задания """
    q = """
SELECT
    m.material
    , IFNULL(lab_material_mark, '') AS lab_material_mark
    , IFNULL(lab_material_group, '') AS lab_material_group
    ,
 arrival.tare_id
    , arrival.tare_mark
    , arrival.tare_type
    ,
 arrival.tare_amount AS arrival_tare_amount
    , arrival.gross_weight AS arrival_gross_weight
    ,
 arrival.tare_amount - IFNULL(P.tare_amount, 0) - IFNULL(S.tare_amount, 0) AS rest_tare_amount
    ,
 arrival.net_weight - IFNULL(P.net_weight, 0) - IFNULL(S.net_weight, 0) + IFNULL(tare.weight, 0) * (
        arrival.tare_amount - IFNULL(P.tare_amount, 0) - IFNULL(S.tare_amount, 0)
    ) AS rest_gross_weight
    ,
 task.tare_amount AS task_tare_amount
    , task.net_weight AS task_net_weight
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
            production_doc.stock = '1'
    ) P
 ON
    P.key_material = arrival.key_material
LEFT JOIN (
        SELECT
            *
        FROM
            shipment
        LEFT JOIN shipment_doc ON
            shipment_doc.id = shipment.doc_id
        WHERE
            shipment_doc.stock = '1'
    ) S
 ON
    S.key_material = arrival.key_material
LEFT JOIN material AS m ON
    m.id = arrival.material
LEFT JOIN tare ON
    arrival.tare_type = tare.id
LEFT JOIN
 (
        SELECT
            lab.key_material
            ,
 TRIM(GROUP_CONCAT(lab.material_mark SEPARATOR ' ')) AS lab_material_mark
            ,
 TRIM(GROUP_CONCAT(lab.material_group SEPARATOR ' ')) AS lab_material_group
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
        FROM
            production_task
        LEFT JOIN production_task_doc ON
            production_task_doc.id = production_task.doc_id
        WHERE
            production_task_doc.id = %(doc_id)s
            AND production_task_doc.stock = '1'
    ) AS task ON
    task.key_material = arrival.key_material
WHERE
    arrival_doc.stock = '1'
    AND
    task.net_weight_fact = 0
    AND
    m.material = "22ИШМБ1810"
ORDER BY
    m.material
    , arrival.tare_id
    """
    result = []
    async with conn.cursor() as cur:
        await cur.execute(q, {"doc_id": doc_id})
        result = await cur.fetchall()
    return result


async def check_user(conn: Connection, login: str, password_hash: str):
    """ проверка авторизации пользователя """
    q = """
SELECT
    s.id
    , s.login
    , s.employee_name
    , s.can_login
FROM
    `MySQL-1248`.staff s
WHERE
    s.login = %(login)s
    AND
    s.password = %(password_hash)s
    """
    result = {}
    async with conn.cursor() as cur:
        await cur.execute(q, {"login": login, "password_hash": password_hash})
        result = await cur.fetchone()
    return result
