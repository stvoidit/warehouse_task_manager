from aiohttp.web import Request, RequestHandler, middleware, ContentCoding

@middleware
async def middleware_compression(request: Request, handler: RequestHandler) -> RequestHandler:
    accept_encoding = request.headers.get("Accept-Encoding")
    resp = await handler(request)
    if accept_encoding is not None:
        if "gzip" in accept_encoding:
            resp.enable_compression(force=ContentCoding.gzip)
        elif "deflate" in accept_encoding:
            resp.enable_compression(force=ContentCoding.deflate)
    return resp
