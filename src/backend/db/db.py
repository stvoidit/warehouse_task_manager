# pylint: disable=too-many-lines

from aiomysql import Connection


async def select_tasks(conn: Connection, user_id: int, stock_id: int):
    """ получение списка заданий """
    q = """
SELECT
    subq.material
    , subq.material_id
    , subq.doc_id
    , subq.doc_number
    , subq.planned_date
    , subq.technical_process
    , subq.operation
    , subq.tare_type
    , subq.category
    , subq.amount
    , IFNULL(ptm.task_weight, subq.weight) AS weight
    , subq.amount_fact
    , subq.weight_fact
FROM
    (
        SELECT
            m.material
            , m.id AS material_id
            , doc.id AS doc_id
            , doc.doc_number
            , doc.planned_date
            , doc.technical_process
            , doc.operation
            , A.tare_type
            , pt.category
            , SUM(pt.tare_amount) AS amount
            , SUM(pt.net_weight) AS weight
            , SUM(pt.tare_amount_fact) AS amount_fact
            , SUM(pt.net_weight_fact) AS weight_fact
        FROM
            production_task pt
        LEFT JOIN production_task_doc AS doc ON
            doc.id = pt.doc_id
        LEFT JOIN material AS m ON
            m.id = pt.material
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
            A.key_material = pt.key_material
        INNER JOIN production_task_executor pte ON
            pte.doc_id = doc.id
        WHERE
            pte.executor_id = %(user_id)s
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
            , A.tare_type
            , pt.category
    ) AS subq
LEFT JOIN production_task_materials ptm ON
    ptm.doc_id = subq.doc_id
    AND ptm.material = subq.material_id
    AND ptm.category = subq.category
ORDER BY
    subq.doc_id ASC
    , subq.material_id ASC
    , subq.category ASC
    , subq.tare_type ASC
    """
    result = []
    async with conn.cursor() as cur:
        await cur.execute(q, { "user_id": user_id, "stock_id": stock_id })
        result = await cur.fetchall()
    return result


async def select_task_meta(conn: Connection, stock_id: int, doc_id: int, material_id: int):
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
INNER JOIN (
        SELECT
            DISTINCT
            pt.doc_id
            , m.material
            , pt.material AS material_id
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
    task.material_id = %(material_id)s
    AND
    ptd.done = 0
    """

    q_categories_materials = """
SELECT
    pt.category
    , GROUP_CONCAT(DISTINCT m.material) AS meterials
FROM
    production_task AS pt
LEFT JOIN material AS m ON
    m.id = pt.material
WHERE
    doc_id = %(doc_id)s
GROUP BY
    pt.category
"""
    task = None
    async with conn.cursor() as cur:
        await cur.execute(q, {"doc_id": doc_id, "stock_id": stock_id, "material_id": material_id})
        task = await cur.fetchone()
        if task is not None:
            catmat = {}
            await cur.execute(q_categories_materials, {"doc_id": doc_id})
            for row in await cur.fetchall():
                catmat[row["category"]] = row["meterials"]
            task["catmat"] = catmat
    return task

async def select_processing_types(conn: Connection):
    q = """SELECT pt.id, pt.process_name FROM processing_type AS pt ORDER BY pt.id ASC"""
    processing_types: list[dict] = []
    async with conn.cursor() as cur:
        await cur.execute(q)
        processing_types.extend(await cur.fetchall())
    return processing_types

async def select_task(conn: Connection, stock_id: int, doc_id: int, material_id: int, tare_type: str):
    """ получение позиций задания """
    task = await select_task_meta(conn, stock_id, doc_id, material_id)
    if task is None:
        return task
    task["task_weights"] = await get_task_weights(conn, doc_id, material_id)
    task["processing_types"] = await select_processing_types(conn)

    q = """
SELECT
    m.material
    , arrival.material as material_id
    , arrival.tare_id
    , arrival.tare_mark
    , arrival.tare_type
    , tare.weight AS tara_weight
    , task.category
    , arrival.net_weight - IFNULL(P.net_weight, 0) - IFNULL(S.net_weight, 0) + IFNULL(tare.weight, 0) * (arrival.tare_amount - IFNULL(P.tare_amount, 0) - IFNULL(S.tare_amount, 0)) AS rest_gross_weight
    , task.tare_amount AS task_tare_amount
    , task.net_weight AS task_net_weight
    , task.net_weight_fact
    , task.add_processing_id
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
            , production_task.category
            , add_processing_id
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
    AND
    tare_type = %(tare_type)s
ORDER BY
    m.material
    , arrival.tare_id
    """
    jobs = []
    query_args = {
            "doc_id": doc_id,
            "stock": stock_id,
            "material_id": material_id,
            "tare_type": tare_type
        }
    async with conn.cursor() as cur:
        await cur.execute(q, query_args)
        jobs = await cur.fetchall()
    task["jobs"] = jobs
    return task


async def get_task_weights(conn: Connection, doc_id: int, material_id: int):
    q1 = """
SELECT
    category
    , task_weight
FROM
    production_task_materials ptm
WHERE
    material = %(material_id)s
    AND doc_id = %(doc_id)s
"""
    q2 = """
SELECT
    category
    , task_weight
FROM
    production_task_categories
WHERE
    doc_id = %(doc_id)s
"""

    task_weights: list[dict] = []
    async with conn.cursor() as cur:
        await cur.execute(q1, {"doc_id": doc_id, "material_id": material_id})
        task_weights = await cur.fetchall()
        # fix: пустой результат возвращает пустой tuple, а не list
        if isinstance(task_weights, tuple):
            task_weights = []
        await cur.execute(q2, {"doc_id": doc_id})
        # проверяем, что если категория есть в списке, то заменяем вес
        # если категории нет, то добавляем
        for row in await cur.fetchall():
            catname: str = row["category"]
            exists = False
            for i, tw in enumerate(task_weights):
                if tw["category"] == catname:
                    task_weights[i] = row
                    exists = True
            if not exists:
                task_weights.append(row)
    return task_weights

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
WHERE
    s.app IS TRUE
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

async def update_job_status(conn: Connection, doc_id: int, user_id: int, material_id: int, tara_id: int, net_weight_fact: float, add_processing_id: int, status: bool):
#     validate_query = """
# SELECT
#     subq.doc_id
#     , subq.material_id
#     , subq.category
#     , IFNULL(ptm.task_weight, subq.weight) - pt_done.net_weight_fact AS remaining_weight
#     , task_job.net_weight AS job_net_weight
#     , task_job.net_weight <= (
#         IFNULL(ptm.task_weight, subq.weight) - pt_done.net_weight_fact
#     ) AS can_done
# FROM
#     (
#         SELECT
#             pt.doc_id
#             , pt.material AS material_id
#             , pt.category
#             , sum(pt.net_weight) AS weight
#         FROM
#             production_task pt
#         WHERE
#             pt.doc_id = %(doc_id)s
#             AND
#             pt.material = %(material_id)s
#             AND pt.category = (
#                 SELECT
#                     category
#                 FROM
#                     production_task
#                 WHERE
#                     tare_id = %(tara_id)s
#                     AND material = %(material_id)s
#             )
#         GROUP BY
#             pt.doc_id
#             , pt.material
#             , pt.category
#     ) AS subq
# LEFT JOIN production_task_materials ptm ON
#     ptm.doc_id = subq.doc_id
#     AND ptm.material = subq.material_id
#     AND ptm.category = subq.category
# INNER JOIN (
#         SELECT
#             pt.doc_id
#             , pt.material AS material_id
#             , pt.category
#             , sum(pt.net_weight_fact) AS net_weight_fact
#         FROM
#             production_task pt
#         WHERE
#             pt.done IS TRUE
#         GROUP BY
#             pt.doc_id
#             , pt.material
#             , pt.category
#     ) pt_done ON
#     pt_done.doc_id = subq.doc_id
#     AND pt_done.material_id = subq.material_id
#     AND pt_done.category = subq.category
# INNER JOIN production_task AS task_job ON
#     task_job.doc_id = subq.doc_id
#     AND
#     task_job.material = subq.material_id
#     AND
#     task_job.category = subq.category
#     AND
#     task_job.tare_id = %(tara_id)s
# """
#     # Валидация доступности действия.
#     # Если статус работы изменяется на "выполнено", то проверяем  превышение веса по задаче в категории.
#     # В случае превышение веса выбрасываем ошибку.
#     can_done = True
#     if status is True:
#         async with conn.cursor() as cur:
#             await cur.execute(validate_query, {"doc_id": doc_id, "material_id": material_id, "tara_id": tara_id})
#             result = await cur.fetchone()
#             print(result)
#             can_done = bool(result["can_done"])
    # if can_done is False:
    #     raise Exception("Превышение веса")

    q = """
UPDATE
    production_task
SET
    done = %(status)s
    , net_weight_fact = CASE WHEN %(status)s IS TRUE THEN %(net_weight_fact)s ELSE 0 END
    , tare_amount_fact = CASE WHEN %(status)s IS TRUE AND %(net_weight_fact)s = net_weight THEN 1 ELSE 0 END
    , fact_executor = CASE WHEN %(status)s IS TRUE THEN %(user_id)s ELSE 0 END
    , add_processing_id = CASE WHEN %(status)s IS TRUE THEN %(add_processing_id)s ELSE 0 END
WHERE
    material = %(material_id)s
    AND
    doc_id = %(doc_id)s
    AND
    tare_id = %(tara_id)s
    """
    query_args = {
        "doc_id": doc_id,
        "user_id": user_id,
        "material_id": material_id,
        "tara_id": tara_id,
        "status": status,
        "net_weight_fact": net_weight_fact,
        "add_processing_id": add_processing_id
    }
    async with conn.cursor() as cur:
        await cur.execute(q, query_args)
    return
