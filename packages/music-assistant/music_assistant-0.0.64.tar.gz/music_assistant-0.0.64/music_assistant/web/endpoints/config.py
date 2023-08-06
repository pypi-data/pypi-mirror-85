"""Config API endpoints."""

from json.decoder import JSONDecodeError

from aiohttp.web import Request, RouteTableDef
from aiohttp_jwt import login_required
from music_assistant.constants import (
    CONF_KEY_BASE,
    CONF_KEY_METADATA_PROVIDERS,
    CONF_KEY_MUSIC_PROVIDERS,
    CONF_KEY_PLAYER_PROVIDERS,
    CONF_KEY_PLAYER_SETTINGS,
    CONF_KEY_PLUGINS,
)
from music_assistant.helpers.web import async_json_response

routes = RouteTableDef()


@routes.get("/api/config")
@login_required
async def async_get_config(request: Request):
    """Get the full config."""
    conf = {
        key: f"/api/config/{key}"
        for key in [
            CONF_KEY_BASE,
            CONF_KEY_MUSIC_PROVIDERS,
            CONF_KEY_PLAYER_PROVIDERS,
            CONF_KEY_METADATA_PROVIDERS,
            CONF_KEY_PLUGINS,
            CONF_KEY_PLAYER_SETTINGS,
        ]
    }
    return await async_json_response(conf)


@routes.get("/api/config/{base}")
@login_required
async def async_get_config_base_item(request: Request):
    """Get the config by base type."""
    language = request.rel_url.query.get("lang", "en")
    conf_base = request.match_info.get("base")
    conf = request.app["mass"].config[conf_base].all_items(language)
    return await async_json_response(conf)


@routes.get("/api/config/{base}/{item}")
@login_required
async def async_get_config_item(request: Request):
    """Get the config by base and item type."""
    language = request.rel_url.query.get("lang", "en")
    conf_base = request.match_info.get("base")
    conf_item = request.match_info.get("item")
    conf = request.app["mass"].config[conf_base][conf_item].all_items(language)
    return await async_json_response(conf)


@routes.put("/api/config/{base}/{key}/{entry_key}")
@login_required
async def async_put_config(request: Request):
    """Save the given config item."""
    conf_key = request.match_info.get("key")
    conf_base = request.match_info.get("base")
    entry_key = request.match_info.get("entry_key")
    try:
        new_value = await request.json()
    except JSONDecodeError:
        new_value = (
            request.app["mass"]
            .config[conf_base][conf_key]
            .get_entry(entry_key)
            .default_value
        )
    request.app["mass"].config[conf_base][conf_key][entry_key] = new_value
    return await async_json_response(
        request.app["mass"].config[conf_base][conf_key][entry_key]
    )
