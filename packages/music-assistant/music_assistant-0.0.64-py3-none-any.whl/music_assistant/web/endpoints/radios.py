"""Tracks API endpoints."""

from aiohttp.web import Request, Response, RouteTableDef
from aiohttp_jwt import login_required
from music_assistant.helpers.web import async_json_response

routes = RouteTableDef()


@routes.get("/api/radios")
@login_required
async def async_radios(request: Request):
    """Get all radios known in the database."""
    return await async_json_response(
        await request.app["mass"].database.async_get_radios()
    )


@routes.get("/api/radios/{item_id}")
@login_required
async def async_radio(request: Request):
    """Get full radio details."""
    item_id = request.match_info.get("item_id")
    provider = request.rel_url.query.get("provider")
    if item_id is None or provider is None:
        return Response(text="invalid item_id or provider", status=501)
    return await async_json_response(
        await request.app["mass"].music.async_get_radio(item_id, provider)
    )
