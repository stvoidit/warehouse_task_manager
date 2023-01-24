from aiohttp import web
from aiohttp.web import middleware


@middleware
async def middleware_check_token(request: web.Request, handler: web.RequestHandler) -> web.RequestHandler:
    print(request.path)
    if request.path != "/api/login":
        token = request.headers.get("token")
        if token is None:
            raise web.HTTPForbidden()
        security = request.app["crypto"]
        security.validate_jwt(token)
    resp = await handler(request)
    return resp
