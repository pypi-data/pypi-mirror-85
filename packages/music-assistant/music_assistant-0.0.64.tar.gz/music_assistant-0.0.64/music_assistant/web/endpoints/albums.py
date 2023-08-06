"""Albums API endpoints."""

from aiohttp.web import Request, Response, RouteTableDef
from aiohttp_jwt import login_required
from music_assistant.helpers.web import async_json_response

routes = RouteTableDef()


@routes.get("/api/albums")
@login_required
async def async_albums(request: Request):
    """Get all albums known in the database."""
    return await async_json_response(
        await request.app["mass"].database.async_get_albums()
    )


@routes.get("/api/albums/{item_id}")
@login_required
async def async_album(request: Request):
    """Get full album details."""
    item_id = request.match_info.get("item_id")
    provider = request.rel_url.query.get("provider")
    if item_id is None or provider is None:
        return Response(text="invalid item or provider", status=501)
    return await async_json_response(
        await request.app["mass"].music.async_get_album(item_id, provider)
    )


@routes.get("/api/albums/{item_id}/tracks")
@login_required
async def async_album_tracks(request: Request):
    """Get album tracks from provider."""
    item_id = request.match_info.get("item_id")
    provider = request.rel_url.query.get("provider")
    if item_id is None or provider is None:
        return Response(text="invalid item_id or provider", status=501)
    return await async_json_response(
        await request.app["mass"].music.async_get_album_tracks(item_id, provider)
    )


@routes.get("/api/albums/{item_id}/versions")
@login_required
async def async_album_versions(request):
    """Get all versions of an album."""
    item_id = request.match_info.get("item_id")
    provider = request.rel_url.query.get("provider")
    if item_id is None or provider is None:
        return Response(text="invalid item_id or provider", status=501)
    return await async_json_response(
        await request.app["mass"].music.async_get_album_versions(item_id, provider)
    )
