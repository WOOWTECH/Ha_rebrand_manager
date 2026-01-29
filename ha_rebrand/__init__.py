"""HA Rebrand - Custom branding for Home Assistant."""
from __future__ import annotations

import logging
import os
import shutil
from functools import partial
from typing import Any

import voluptuous as vol

from homeassistant.components import panel_custom
from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ha_rebrand"
CONF_BRAND_NAME = "brand_name"
CONF_LOGO = "logo"
CONF_LOGO_DARK = "logo_dark"
CONF_FAVICON = "favicon"
CONF_REPLACEMENTS = "replacements"
CONF_SIDEBAR_TITLE = "sidebar_title"
CONF_DOCUMENT_TITLE = "document_title"

DEFAULT_BRAND_NAME = "Home Assistant"
DEFAULT_REPLACEMENTS = {
    "Home Assistant": "Home Assistant",
}

# Security constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_FILE_TYPES = {"logo", "logo_dark", "favicon"}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp"}

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_BRAND_NAME, default=DEFAULT_BRAND_NAME): cv.string,
                vol.Optional(CONF_LOGO): cv.string,
                vol.Optional(CONF_LOGO_DARK): cv.string,
                vol.Optional(CONF_FAVICON): cv.string,
                vol.Optional(CONF_SIDEBAR_TITLE): cv.string,
                vol.Optional(CONF_DOCUMENT_TITLE): cv.string,
                vol.Optional(CONF_REPLACEMENTS, default={}): vol.Schema(
                    {cv.string: cv.string}
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HA Rebrand component."""
    conf = config.get(DOMAIN, {})

    # Debug logging
    _LOGGER.info("HA Rebrand config from YAML: %s", conf)
    _LOGGER.info("HA Rebrand replacements from YAML: %s", conf.get(CONF_REPLACEMENTS, {}))

    # Store configuration
    hass.data[DOMAIN] = {
        CONF_BRAND_NAME: conf.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
        CONF_LOGO: conf.get(CONF_LOGO),
        CONF_LOGO_DARK: conf.get(CONF_LOGO_DARK),
        CONF_FAVICON: conf.get(CONF_FAVICON),
        CONF_SIDEBAR_TITLE: conf.get(CONF_SIDEBAR_TITLE, conf.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME)),
        CONF_DOCUMENT_TITLE: conf.get(CONF_DOCUMENT_TITLE, conf.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME)),
        CONF_REPLACEMENTS: {**DEFAULT_REPLACEMENTS, **conf.get(CONF_REPLACEMENTS, {})},
        "uploads_dir": hass.config.path("www", "ha_rebrand"),
    }

    _LOGGER.info("HA Rebrand final config: %s", hass.data[DOMAIN])

    # Create uploads directory
    uploads_dir = hass.data[DOMAIN]["uploads_dir"]
    await hass.async_add_executor_job(_create_directory, uploads_dir)

    # Write config to static JSON file for injector
    config_json = {
        "brand_name": hass.data[DOMAIN].get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
        "logo": hass.data[DOMAIN].get(CONF_LOGO),
        "logo_dark": hass.data[DOMAIN].get(CONF_LOGO_DARK),
        "favicon": hass.data[DOMAIN].get(CONF_FAVICON),
        "sidebar_title": hass.data[DOMAIN].get(CONF_SIDEBAR_TITLE),
        "document_title": hass.data[DOMAIN].get(CONF_DOCUMENT_TITLE),
        "replacements": hass.data[DOMAIN].get(CONF_REPLACEMENTS, {}),
    }
    config_json_path = os.path.join(uploads_dir, "config.json")
    await hass.async_add_executor_job(_write_config_json, config_json_path, config_json)
    _LOGGER.info("HA Rebrand config written to %s", config_json_path)

    # Register frontend resources
    await _async_register_frontend(hass)

    # Register HTTP views
    _LOGGER.error("!!! Registering RebrandConfigView for /api/ha_rebrand/config !!!")
    hass.http.register_view(RebrandConfigView(hass))
    hass.http.register_view(RebrandUploadView(hass))
    hass.http.register_view(RebrandSaveConfigView(hass))
    _LOGGER.error("!!! All views registered !!!")

    # Register panel
    await panel_custom.async_register_panel(
        hass,
        webcomponent_name="ha-rebrand-panel",
        frontend_url_path="ha-rebrand",
        config_panel_domain=DOMAIN,
        sidebar_title="Rebrand",
        sidebar_icon="mdi:palette-outline",
        module_url="/ha_rebrand/ha-rebrand-panel.js",
        embed_iframe=False,
        require_admin=True,
    )

    # Register WebSocket commands
    _async_register_websocket_commands(hass)

    _LOGGER.info("HA Rebrand component loaded successfully")
    return True


def _create_directory(path: str) -> None:
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def _write_config_json(path: str, config: dict) -> None:
    """Write config to JSON file for static serving."""
    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def _copy_frontend_files(frontend_src: str, frontend_dest: str) -> None:
    """Copy frontend files to destination."""
    if not os.path.exists(frontend_dest):
        os.makedirs(frontend_dest, exist_ok=True)

    for filename in os.listdir(frontend_src):
        src_file = os.path.join(frontend_src, filename)
        dest_file = os.path.join(frontend_dest, filename)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dest_file)


async def _async_register_frontend(hass: HomeAssistant) -> None:
    """Register frontend resources."""
    component_dir = os.path.dirname(__file__)
    frontend_src = os.path.join(component_dir, "frontend")
    frontend_dest = hass.config.path("www", "ha_rebrand")

    # Copy frontend files using executor
    await hass.async_add_executor_job(_copy_frontend_files, frontend_src, frontend_dest)

    # Register the rebrand static path using new API
    await hass.http.async_register_static_paths([
        StaticPathConfig("/ha_rebrand", frontend_dest, cache_headers=False)
    ])


@callback
def _async_register_websocket_commands(hass: HomeAssistant) -> None:
    """Register WebSocket commands."""
    from homeassistant.components import websocket_api

    @websocket_api.websocket_command({
        vol.Required("type"): "ha_rebrand/get_config",
    })
    @callback
    def websocket_get_config(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        """Get rebrand configuration."""
        config = hass.data.get(DOMAIN, {})
        connection.send_result(msg["id"], {
            "brand_name": config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
            "logo": config.get(CONF_LOGO),
            "logo_dark": config.get(CONF_LOGO_DARK),
            "favicon": config.get(CONF_FAVICON),
            "sidebar_title": config.get(CONF_SIDEBAR_TITLE),
            "document_title": config.get(CONF_DOCUMENT_TITLE),
            "replacements": config.get(CONF_REPLACEMENTS, {}),
        })

    @websocket_api.websocket_command({
        vol.Required("type"): "ha_rebrand/update_config",
        vol.Optional("brand_name"): cv.string,
        vol.Optional("logo"): vol.Any(cv.string, None),
        vol.Optional("logo_dark"): vol.Any(cv.string, None),
        vol.Optional("favicon"): vol.Any(cv.string, None),
        vol.Optional("sidebar_title"): cv.string,
        vol.Optional("document_title"): cv.string,
        vol.Optional("replacements"): vol.Schema({cv.string: cv.string}),
    })
    @websocket_api.require_admin
    @websocket_api.async_response
    async def websocket_update_config(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        """Update rebrand configuration. Requires admin privileges."""
        _LOGGER.warning("WebSocket update_config called with: %s", msg)
        config = hass.data.get(DOMAIN, {})

        if "brand_name" in msg:
            config[CONF_BRAND_NAME] = msg["brand_name"]
        if "logo" in msg:
            config[CONF_LOGO] = msg["logo"]
        if "logo_dark" in msg:
            config[CONF_LOGO_DARK] = msg["logo_dark"]
        if "favicon" in msg:
            config[CONF_FAVICON] = msg["favicon"]
        if "sidebar_title" in msg:
            config[CONF_SIDEBAR_TITLE] = msg["sidebar_title"]
        if "document_title" in msg:
            config[CONF_DOCUMENT_TITLE] = msg["document_title"]
        if "replacements" in msg:
            config[CONF_REPLACEMENTS] = msg["replacements"]

        hass.data[DOMAIN] = config

        # Write updated config to static JSON file
        config_json = {
            "brand_name": config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
            "logo": config.get(CONF_LOGO),
            "logo_dark": config.get(CONF_LOGO_DARK),
            "favicon": config.get(CONF_FAVICON),
            "sidebar_title": config.get(CONF_SIDEBAR_TITLE),
            "document_title": config.get(CONF_DOCUMENT_TITLE),
            "replacements": config.get(CONF_REPLACEMENTS, {}),
        }
        uploads_dir = config.get("uploads_dir", hass.config.path("www", "ha_rebrand"))
        config_json_path = os.path.join(uploads_dir, "config.json")
        await hass.async_add_executor_job(_write_config_json, config_json_path, config_json)
        _LOGGER.info("HA Rebrand config updated and written to %s", config_json_path)

        connection.send_result(msg["id"], {"success": True})

    websocket_api.async_register_command(hass, websocket_get_config)
    websocket_api.async_register_command(hass, websocket_update_config)


class RebrandConfigView(HomeAssistantView):
    """View to get rebrand configuration via HTTP.

    Note: This endpoint returns minimal branding data for the injector script.
    Full configuration requires authentication via WebSocket API.
    """

    url = "/api/ha_rebrand/brand_config"
    name = "api:ha_rebrand:brand_config"
    requires_auth = False  # Allow unauthenticated access for injector script

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self.hass = hass

    async def get(self, request):
        """Handle GET request."""
        import logging
        logger = logging.getLogger("custom_components.ha_rebrand")
        config = self.hass.data.get(DOMAIN, {})
        logger.error("!!! API GET /api/ha_rebrand/config called !!!")
        logger.error("!!! Current hass.data[DOMAIN] = %s", config)
        return self.json({
            "brand_name": config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
            "logo": config.get(CONF_LOGO),
            "logo_dark": config.get(CONF_LOGO_DARK),
            "favicon": config.get(CONF_FAVICON),
            "sidebar_title": config.get(CONF_SIDEBAR_TITLE),
            "document_title": config.get(CONF_DOCUMENT_TITLE),
            "replacements": config.get(CONF_REPLACEMENTS, {}),
        })


class RebrandUploadView(HomeAssistantView):
    """View to handle file uploads with security validations."""

    url = "/api/ha_rebrand/upload"
    name = "api:ha_rebrand:upload"
    requires_auth = True

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self.hass = hass

    async def post(self, request):
        """Handle file upload with security checks."""
        # Check if user is admin
        if not request["hass_user"].is_admin:
            return self.json({"error": "Admin privileges required"}, status_code=403)

        data = await request.post()
        file_field = data.get("file")
        file_type = data.get("type", "logo")

        if not file_field:
            return self.json({"error": "No file provided"}, status_code=400)

        # Validate file_type against allowlist
        if file_type not in ALLOWED_FILE_TYPES:
            return self.json(
                {"error": f"Invalid file type. Allowed: {', '.join(ALLOWED_FILE_TYPES)}"},
                status_code=400
            )

        # Get and validate file extension
        filename = file_field.filename
        ext = os.path.splitext(filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            return self.json(
                {"error": f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"},
                status_code=400
            )

        # Read file with size limit
        content = file_field.file.read(MAX_FILE_SIZE + 1)
        if len(content) > MAX_FILE_SIZE:
            return self.json(
                {"error": f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB."},
                status_code=400
            )

        # Save file using executor to avoid blocking
        uploads_dir = self.hass.data[DOMAIN]["uploads_dir"]
        new_filename = f"{file_type}{ext}"
        file_path = os.path.join(uploads_dir, new_filename)

        await self.hass.async_add_executor_job(
            partial(self._write_file, file_path, content)
        )

        # Return the URL path
        url_path = f"/local/ha_rebrand/{new_filename}"

        return self.json({
            "success": True,
            "path": url_path,
            "filename": new_filename,
        })

    @staticmethod
    def _write_file(file_path: str, content: bytes) -> None:
        """Write file to disk."""
        with open(file_path, "wb") as f:
            f.write(content)


class RebrandSaveConfigView(HomeAssistantView):
    """View to save configuration to file."""

    url = "/api/ha_rebrand/save_config"
    name = "api:ha_rebrand:save_config"
    requires_auth = True

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self.hass = hass

    async def post(self, request):
        """Save configuration to ha_rebrand.yaml."""
        # Check if user is admin
        if not request["hass_user"].is_admin:
            return self.json({"error": "Admin privileges required"}, status_code=403)

        import yaml

        config = self.hass.data.get(DOMAIN, {})

        # Prepare config for YAML
        yaml_config: dict[str, Any] = {
            DOMAIN: {
                CONF_BRAND_NAME: config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
            }
        }

        if config.get(CONF_LOGO):
            yaml_config[DOMAIN][CONF_LOGO] = config[CONF_LOGO]
        if config.get(CONF_LOGO_DARK):
            yaml_config[DOMAIN][CONF_LOGO_DARK] = config[CONF_LOGO_DARK]
        if config.get(CONF_FAVICON):
            yaml_config[DOMAIN][CONF_FAVICON] = config[CONF_FAVICON]
        if config.get(CONF_SIDEBAR_TITLE):
            yaml_config[DOMAIN][CONF_SIDEBAR_TITLE] = config[CONF_SIDEBAR_TITLE]
        if config.get(CONF_DOCUMENT_TITLE):
            yaml_config[DOMAIN][CONF_DOCUMENT_TITLE] = config[CONF_DOCUMENT_TITLE]
        if config.get(CONF_REPLACEMENTS):
            yaml_config[DOMAIN][CONF_REPLACEMENTS] = config[CONF_REPLACEMENTS]

        # Write to file using executor to avoid blocking
        config_path = self.hass.config.path("ha_rebrand.yaml")
        await self.hass.async_add_executor_job(
            partial(self._write_yaml, config_path, yaml_config)
        )

        return self.json({
            "success": True,
            "path": config_path,
            "message": "Configuration saved. Add 'ha_rebrand: !include ha_rebrand.yaml' to configuration.yaml and restart.",
        })

    @staticmethod
    def _write_yaml(config_path: str, yaml_config: dict) -> None:
        """Write YAML configuration to file."""
        import yaml
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(yaml_config, f, default_flow_style=False, allow_unicode=True)
