import jwt
from aiohttp.web import HTTPForbidden, Request, RequestHandler, middleware

from db import check_can_login

@middleware
async def middleware_check_token(request: Request, handler: RequestHandler) -> RequestHandler:
    """
        Проверка авторизации пользователя, валидация токена.

        Если запрос идет на /api - это нужные для валидации запросы.
        Остальные - это запросы на статику (фронт).

        * Если в заголовке нет токена, то возвращаем 403
        * Валидируем токен пользователя, если он просрочен или подпись неверна, то возвращаем 403

        В случае успешной валидации, извлекаем из токена данные о пользователе (нас интересует только его id)?
        и передаем этот id далее в запросе, чтобы делать по нему запросы в БД.
    """
    if request.path != "/api/login" and request.path.startswith("/api"):
        token = request.headers.get("token")
        if token is None:
            raise HTTPForbidden()
        security = request.app["crypto"]
        try:
            decoded_token = security.validate_jwt(token)
            if decoded_token.get("payload"):
                user_id = decoded_token.get("payload").get("id")
                async with request.app["db"].acquire() as conn:
                    can_login = await check_can_login(conn, user_id)
                    if can_login is False:
                        raise HTTPForbidden()
                request.user_id = user_id
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError) as exc:
            raise HTTPForbidden(reason=exc) # pylint: disable=raise-missing-from
    resp = await handler(request)
    return resp
