from aiohttp import web
from aiohttp.web import middleware
import jwt

@middleware
async def middleware_check_token(request: web.Request, handler: web.RequestHandler) -> web.RequestHandler:
    if request.path != "/api/login" and request.path.startswith("/api"):
        token = request.headers.get("token")
        if token is None:
            raise web.HTTPForbidden()
        security = request.app["crypto"]
        try:
            security.validate_jwt(token)
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError):
            raise web.HTTPForbidden()
    resp = await handler(request)
    return resp
