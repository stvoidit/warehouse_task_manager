# pylint: disable=too-many-lines

from aiomysql import Connection


async def select_tasks(conn: Connection, user_id: int, stock_id: int) -> list:
    """ получение списка заданий """
    q = """
SELECT
    doc_id
    , material_id
    , material
    , category
    , planned_date
    , technical_process
    , operation
    , tare_amount
    , task_weight AS weight
    , tare_amount_fact
    , net_weight_fact
    , IF(
        task_weight > 0
        , IF(
            net_weight_fact >= task_weight
            , 1
            , 0
        )
        , cat_done
    ) AS done
FROM
    (
        SELECT
            doc_id
            , material_id
            , material
            , category
            , planned_date
            , technical_process
            , operation
            , tare_amount
            , IF(
                task_weight_category = 0
                , IF(
                    task_weight_material = 0
                    , net_weight
                    , task_weight_material
                )
                , 0
            ) AS task_weight
            , tare_amount_fact
            , net_weight_fact
            , cat_done
        FROM
            (
                SELECT
                    ptm.doc_id
                    , ptm.material AS material_id
                    , m.material
                    , ptm.category
                    , pt.planned_date
                    , pt.technical_process
                    , pt.operation
                    , ptm.task_weight AS task_weight_material
                    , IFNULL(ptc.task_weight, 0) AS task_weight_category
                    , pt.tare_amount
                    , pt.net_weight
                    , pt.tare_amount_fact
                    , pt.net_weight_fact
                FROM
                    production_task_materials AS ptm
                LEFT JOIN production_task_categories AS ptc ON
                    ptm.doc_id = ptc.doc_id
                    AND ptm.category = ptc.category
                LEFT JOIN material AS m ON
                    m.id = ptm.material
                INNER JOIN
                (
                    SELECT
                        pt.doc_id
                        , material
                        , category
                        , ptd.planned_date AS planned_date
                        , ptd.technical_process AS technical_process
                        , ptd.operation AS operation
                        , SUM(tare_amount) AS tare_amount
                        , SUM(net_weight) AS net_weight
                        , SUM(tare_amount_fact) AS tare_amount_fact
                        , SUM(net_weight_fact) AS net_weight_fact
                    FROM
                        production_task AS pt
                    LEFT JOIN production_task_doc AS ptd ON
                        ptd.id = pt.doc_id
                    LEFT JOIN production_task_executor AS pte ON
                        pte.doc_id = pt.doc_id
                    WHERE
                        pte.executor_id = %(user_id)s
                        AND ptd.done = 0
                    GROUP BY
                        doc_id
                        , material
                        , category
                        , planned_date
                        , technical_process
                        , operation
                ) pt ON
                pt.doc_id = ptm.doc_id
                AND pt.material = ptm.material
                AND pt.category = ptm.category
            ) task_list
        LEFT JOIN
        (
                SELECT
                    subq.doc_id AS cat_doc_id
                    , subq.category AS cat_category
                    , IF(
                        subq.weight_fact >= ptc.task_weight
                        , 1
                        , 0
                    ) AS cat_done
                FROM
                    (
                        SELECT
                            doc.id AS doc_id
                            , pt.category
                            , SUM(pt.net_weight) AS weight
                            , SUM(pt.net_weight_fact) AS weight_fact
                        FROM
                            production_task pt
                        INNER JOIN production_task_doc AS doc ON
                            doc.id = pt.doc_id
                            AND
                            doc.stock = %(stock_id)s
                        LEFT JOIN material AS m ON
                            m.id = pt.material
                        INNER JOIN production_task_executor pte ON
                            pte.doc_id = doc.id
                        WHERE
                            pte.executor_id = %(user_id)s
                            AND
                            doc.done = 0
                        GROUP BY
                            doc.id
                            , doc.doc_number
                            , doc.planned_date
                            , doc.technical_process
                            , doc.operation
                            , pt.category
                    ) AS subq
                INNER JOIN production_task_categories ptc ON
                    ptc.doc_id = subq.doc_id
                    AND ptc.category = subq.category
                    AND ptc.task_weight > 0
            ) cat ON
            cat.cat_doc_id = task_list.doc_id
            AND
            cat.cat_category = task_list.category
    ) task_list
ORDER BY
    doc_id
    , material
    , category
    """
    result = []
    async with conn.cursor() as cur:
        await cur.execute(q, {"user_id": user_id, "stock_id": stock_id})
        result = await cur.fetchall()
        if isinstance(result, tuple):
            result = []
    return result


async def select_tasks_progress(conn: Connection, user_id: int, stock_id: int) -> list:
    q = """
SELECT
    subq.material
    , subq.doc_id
    , subq.doc_number
    , subq.planned_date
    , subq.technical_process
    , subq.operation
    , subq.category
    , subq.amount
    , ptc.task_weight AS weight
    , subq.amount_fact
    , subq.weight_fact
    , IF(
        subq.weight_fact >= ptc.task_weight
        , 1
        , 0
    ) AS done
FROM
    (
        SELECT
            doc.id AS doc_id
            , doc.doc_number
            , doc.planned_date
            , doc.technical_process
            , doc.operation
            , pt.category
            , GROUP_CONCAT(
                DISTINCT m.material
            ) AS material
            , SUM(pt.tare_amount) AS amount
            , SUM(pt.net_weight) AS weight
            , SUM(pt.tare_amount_fact) AS amount_fact
            , SUM(pt.net_weight_fact) AS weight_fact
        FROM
            production_task pt
        INNER JOIN production_task_doc AS doc ON
            doc.id = pt.doc_id
            AND
            doc.stock = %(stock_id)s
        LEFT JOIN material AS m ON
            m.id = pt.material
        INNER JOIN production_task_executor pte ON
            pte.doc_id = doc.id
        WHERE
            pte.executor_id = %(user_id)s
            AND
            doc.done = 0
        GROUP BY
            doc.id
            , doc.doc_number
            , doc.planned_date
            , doc.technical_process
            , doc.operation
            , pt.category
    ) AS subq
INNER JOIN production_task_categories ptc ON
    ptc.doc_id = subq.doc_id
    AND ptc.category = subq.category
    AND ptc.task_weight > 0
ORDER BY
    subq.doc_id ASC
    , subq.category ASC
"""
    result = []
    async with conn.cursor() as cur:
        await cur.execute(q, {"user_id": user_id, "stock_id": stock_id})
        result = await cur.fetchall()
        if isinstance(result, tuple):
            result = []
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
    , GROUP_CONCAT(DISTINCT m.material SEPARATOR ';') AS meterials
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


async def select_task(conn: Connection, stock_id: int, doc_id: int, material_id: int, user_id: int):
    """ получение позиций задания """
    task = await select_task_meta(conn, stock_id, doc_id, material_id)
    if task is None:
        return task
    task["task_weights"] = await get_task_weights(conn, doc_id, material_id, user_id)
    task["processing_types"] = await select_processing_types(conn)

    q = """
SELECT
    m.material
    , sd.material AS material_id
    , sd.tare_id
    , sd.tare_mark
    , sd.tare_type
    , sd.tare_weight AS tara_weight
    , task.category
    , IF(task.gross_weight = 0, sd.rest_gross_weight, task.gross_weight) AS rest_gross_weight
    , task.tare_amount AS task_tare_amount
    , task.net_weight AS task_net_weight
    , task.net_weight_fact
    , task.add_processing_id
    , task.done
FROM
(
    SELECT
        sd.*
        , md.tare_type
        , md.tare_mark
        , md.material_group
        , md.material_mark
        , sd.rest_net_weight + sd.rest_tare_amount * tare.weight AS rest_gross_weight
        , tare.weight AS tare_weight
    FROM
    (
        SELECT
            stock
            , material
            , tare_id
            , key_material
            , SUM(tare_amount) AS rest_tare_amount
            , SUM(net_weight) AS rest_net_weight
        FROM stock_data AS sd
        GROUP BY stock, material, tare_id, key_material
    ) sd
    LEFT JOIN
        material_data AS md ON md.key_material = sd.key_material
    LEFT JOIN
        tare ON tare.id = md.tare_type
) sd
LEFT JOIN material_data AS md ON
    md.key_material = sd.key_material
LEFT JOIN material AS m ON
    m.id = sd.material
INNER JOIN (
        SELECT
            key_material
            , tare_amount
            , net_weight
            , gross_weight
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
    AND production_task_doc.stock = %(stock_id)s
) AS task ON
    task.key_material = sd.key_material
WHERE
    stock =  %(stock_id)s
    AND
    sd.material = %(material_id)s
ORDER BY
    m.material
    , sd.tare_id
    """
    jobs = []
    query_args = {
        "doc_id": doc_id,
        "stock_id": stock_id,
        "material_id": material_id
    }
    async with conn.cursor() as cur:
        await cur.execute(q, query_args)
        jobs = await cur.fetchall()
    task["jobs"] = jobs
    return task


async def get_task_weights(conn: Connection, doc_id: int, material_id: int, user_id: int):
    q1 = """
SELECT
    doc_id
    , material_id
    , material
    , category
    , tare_amount
    , task_weight_category AS task_weight
    , tare_amount_fact
    , net_weight_fact
    , category_details
FROM
    (
        SELECT
            ptm.doc_id
            , ptm.material AS material_id
            , m.material
            , ptm.category
            , ptm.task_weight AS task_weight_material
            , ptc.task_weight AS task_weight_category
            , pt.tare_amount
            , pt.net_weight
            , pt.tare_amount_fact
            , pt.net_weight_fact
        FROM
            production_task_materials AS ptm
        LEFT JOIN production_task_categories AS ptc ON
            ptm.doc_id = ptc.doc_id
            AND ptm.category = ptc.category
        LEFT JOIN material AS m ON
            m.id = ptm.material
        INNER JOIN
            (
                SELECT
                    pt.doc_id
                    , category
                    , SUM(tare_amount) AS tare_amount
                    , SUM(net_weight) AS net_weight
                    , SUM(tare_amount_fact) AS tare_amount_fact
                    , SUM(net_weight_fact) AS net_weight_fact
                FROM
                    production_task AS pt
                LEFT JOIN production_task_doc AS ptd ON
                    ptd.id = pt.doc_id
                LEFT JOIN production_task_executor AS pte ON
                    pte.doc_id = pt.doc_id
                WHERE
                    pte.executor_id = %(user_id)s
                    AND ptd.done = 0
                GROUP BY
                    doc_id
                    , category
            ) pt ON
            pt.doc_id = ptm.doc_id
            AND pt.category = ptm.category
        WHERE
            ptm.doc_id = %(doc_id)s
            AND ptm.material = %(material_id)s
            AND NOT ptc.task_weight IS NULL
    ) task_list
LEFT JOIN
        (
        SELECT
                ptc.doc_id AS category_details_doc_id
            , ptc.category AS category_details_category
            , GROUP_CONCAT(m.material) AS category_details
        FROM
                production_task_categories AS ptc
        LEFT JOIN production_task_materials AS ptm ON
                ptm.doc_id = ptc.doc_id
            AND ptm.category = ptc.category
        LEFT JOIN material AS m ON
                m.id = ptm.material
        GROUP BY
            category_details_doc_id
            , category_details_category
    ) details ON
        details.category_details_doc_id = task_list.doc_id
    AND details.category_details_category = task_list.category
UNION ALL
SELECT
    doc_id
    , material_id
    , material
    , category
    , tare_amount
    , IF(
        task_weight_material = 0
        , net_weight
        , task_weight_material
    ) AS task_weight
    , tare_amount_fact
    , net_weight_fact
    , material AS category_details
FROM
    (
        SELECT
            ptm.doc_id
            , ptm.material AS material_id
            , ptm.category
            , m.material
            , ptm.task_weight AS task_weight_material
            , pt.tare_amount
            , pt.net_weight
            , pt.tare_amount_fact
            , pt.net_weight_fact
        FROM
            (
                SELECT
                    ptm.*
                FROM
                    production_task_materials AS ptm
                LEFT JOIN production_task_categories AS ptc ON
                    ptc.doc_id = ptm.doc_id
                    AND ptc.category = ptm.category
                WHERE
                    ptc.category IS NULL
            ) ptm
        LEFT JOIN material AS m ON
            m.id = ptm.material
        INNER JOIN
            (
                SELECT
                    pt.doc_id
                    , material
                    , category
                    , SUM(tare_amount) AS tare_amount
                    , SUM(net_weight) AS net_weight
                    , SUM(tare_amount_fact) AS tare_amount_fact
                    , SUM(net_weight_fact) AS net_weight_fact
                FROM
                    production_task AS pt
                LEFT JOIN production_task_doc AS ptd ON
                    ptd.id = pt.doc_id
                LEFT JOIN production_task_executor AS pte ON
                    pte.doc_id = pt.doc_id
                WHERE
                    pte.executor_id = %(user_id)s
                    AND ptd.done = 0
                GROUP BY
                    doc_id
                    , material
                    , category
            ) pt ON
            pt.doc_id = ptm.doc_id
            AND pt.material = ptm.material
            AND pt.category = ptm.category
        WHERE
            ptm.doc_id = %(doc_id)s
            AND ptm.material = %(material_id)s
    ) task_list
"""
    params = {
        "doc_id": doc_id,
        "material_id": material_id,
        "user_id": user_id
    }
    task_weights: list[dict] = []
    async with conn.cursor() as cur:
        await cur.execute(q1, params)
        task_weights = await cur.fetchall()
        # fix: пустой результат возвращает пустой tuple, а не list
        if isinstance(task_weights, tuple):
            task_weights = []
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
    , tare_amount_fact = CASE WHEN %(status)s IS TRUE AND (%(net_weight_fact)s = net_weight OR net_weight = 0) THEN 1 ELSE 0 END
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
        # На всякий случай перехват ошибки, чтобы совсем не падать
        try:
            await cur.callproc("update_next_process_v2", [doc_id, material_id, tara_id])
        except Exception as e:
            print(f"ERROR callproc \"update_next_process\": {e}")
    return


async def update_rest_gross_weight(conn: Connection, doc_id: int, material_id: int, tare_id: int, gross_weight: float):
    q = """
UPDATE production_task
SET
    gross_weight = %(gross_weight)s
WHERE
    doc_id = %(doc_id)s
    AND
    material = %(material_id)s
    AND
    tare_id = %(tare_id)s
    """
    async with conn.cursor() as cur:
        await cur.execute(q, {
            "doc_id": doc_id,
            "material_id": material_id,
            "tare_id": tare_id,
            "gross_weight": gross_weight
        })
