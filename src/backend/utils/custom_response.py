import datetime
from decimal import Decimal
from io import BytesIO
from typing import Any

import orjson
from aiohttp.web import Request, Response


async def jsonify(
        data: Any,
        request: Request,
        status: int = 200,
        content_type: str = 'application/json') -> Response:
    """ Кастомная обертка для формирования Reponse в формате json с сжатием """
    def serializer(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError
    body = orjson.dumps(  # pylint: disable=no-member
        data,
        option=orjson.OPT_OMIT_MICROSECONDS | orjson.OPT_PASSTHROUGH_DATETIME,  # pylint: disable=no-member
        default=serializer)
    response = Response(text=None,
                        body=body,
                        status=status,
                        content_type=content_type)
    await response.prepare(request)
    return response


async def send_file(buf: BytesIO, filename: str, request: Request) -> Response:
    """ Унифицированный ответ для отправки файла в ответ """
    headers = {
        "content-disposition": f'attachment; filename="{filename}"',
        "content-type": "application/octet-stream"
    }
    response = Response(body=buf, headers=headers)
    await response.prepare(request)
    return response
