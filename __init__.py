"""HA Rebrand - Custom branding for Home Assistant."""
from __future__ import annotations

import json
import logging
import os
import shutil
from functools import partial
from typing import Any

import voluptuous as vol

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    CONF_BRAND_NAME,
    CONF_LOGO,
    CONF_LOGO_DARK,
    CONF_FAVICON,
    CONF_REPLACEMENTS,
    CONF_SIDEBAR_TITLE,
    CONF_DOCUMENT_TITLE,
    CONF_HIDE_OPEN_HOME_FOUNDATION,
    DEFAULT_BRAND_NAME,
    DEFAULT_REPLACEMENTS,
    MAX_FILE_SIZE,
    ALLOWED_FILE_TYPES,
    ALLOWED_EXTENSIONS,
    PANEL_URL_PATH,
    PANEL_COMPONENT_NAME,
    PANEL_TITLE,
    PANEL_ICON,
)

_LOGGER = logging.getLogger(__name__)

type HaRebrandConfigEntry = ConfigEntry

DATA_PANEL_REGISTERED = f"{DOMAIN}_panel_registered"

# Keep CONFIG_SCHEMA for backward compatibility (YAML still works)
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
    """Set up the HA Rebrand component (YAML configuration)."""
    hass.data.setdefault(DOMAIN, {})

    # Register WebSocket API at setup level (available for all entries)
    _async_register_websocket_commands(hass)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: HaRebrandConfigEntry) -> bool:
    """Set up HA Rebrand from a config entry."""
    _LOGGER.info("Setting up HA Rebrand from config entry")

    # Initialize data structure
    hass.data.setdefault(DOMAIN, {})

    # Create uploads directory
    uploads_dir = hass.config.path("www", "ha_rebrand")
    await hass.async_add_executor_job(_create_directory, uploads_dir)

    # Load existing config from JSON file if exists
    config_json_path = os.path.join(uploads_dir, "config.json")
    config = await hass.async_add_executor_job(_load_config_json, config_json_path)

    # Store configuration in hass.data
    hass.data[DOMAIN] = {
        CONF_BRAND_NAME: config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
        CONF_LOGO: config.get(CONF_LOGO),
        CONF_LOGO_DARK: config.get(CONF_LOGO_DARK),
        CONF_FAVICON: config.get(CONF_FAVICON),
        CONF_SIDEBAR_TITLE: config.get(CONF_SIDEBAR_TITLE, config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME)),
        CONF_DOCUMENT_TITLE: config.get(CONF_DOCUMENT_TITLE, config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME)),
        CONF_REPLACEMENTS: config.get(CONF_REPLACEMENTS, DEFAULT_REPLACEMENTS),
        CONF_HIDE_OPEN_HOME_FOUNDATION: config.get(CONF_HIDE_OPEN_HOME_FOUNDATION, True),
        "uploads_dir": uploads_dir,
    }

    # Write initial config.json
    await _async_write_config_json(hass)

    # Register frontend resources
    await _async_register_frontend(hass)

    # Register HTTP views
    hass.http.register_view(RebrandConfigView(hass))
    hass.http.register_view(RebrandUploadView(hass))
    hass.http.register_view(RebrandSaveConfigView(hass))

    # Register panel (only once)
    if not hass.data.get(DATA_PANEL_REGISTERED):
        await panel_custom.async_register_panel(
            hass,
            webcomponent_name=PANEL_COMPONENT_NAME,
            frontend_url_path=PANEL_URL_PATH,
            config_panel_domain=DOMAIN,
            sidebar_title=PANEL_TITLE,
            sidebar_icon=PANEL_ICON,
            module_url="/ha_rebrand/ha-rebrand-panel.js",
            embed_iframe=False,
            require_admin=True,
        )
        hass.data[DATA_PANEL_REGISTERED] = True

    _LOGGER.info("HA Rebrand component loaded successfully")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: HaRebrandConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading HA Rebrand")

    # Unregister panel
    if hass.data.get(DATA_PANEL_REGISTERED):
        if PANEL_URL_PATH in hass.data.get(frontend.DATA_PANELS, {}):
            frontend.async_remove_panel(hass, PANEL_URL_PATH)
        hass.data[DATA_PANEL_REGISTERED] = False

    # Clean up hass.data but keep uploads_dir reference
    uploads_dir = hass.data.get(DOMAIN, {}).get("uploads_dir")
    hass.data[DOMAIN] = {"uploads_dir": uploads_dir} if uploads_dir else {}

    return True


def _create_directory(path: str) -> None:
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def _load_config_json(path: str) -> dict:
    """Load config from JSON file."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _write_config_json(path: str, config: dict) -> None:
    """Write config to JSON file for static serving."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


async def _async_write_config_json(hass: HomeAssistant) -> None:
    """Write current config to JSON file."""
    config = hass.data.get(DOMAIN, {})
    config_json = {
        "brand_name": config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
        "logo": config.get(CONF_LOGO),
        "logo_dark": config.get(CONF_LOGO_DARK),
        "favicon": config.get(CONF_FAVICON),
        "sidebar_title": config.get(CONF_SIDEBAR_TITLE),
        "document_title": config.get(CONF_DOCUMENT_TITLE),
        "replacements": config.get(CONF_REPLACEMENTS, {}),
        "hide_open_home_foundation": config.get(CONF_HIDE_OPEN_HOME_FOUNDATION, True),
    }
    uploads_dir = config.get("uploads_dir", hass.config.path("www", "ha_rebrand"))
    config_json_path = os.path.join(uploads_dir, "config.json")
    await hass.async_add_executor_job(_write_config_json, config_json_path, config_json)


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
            "hide_open_home_foundation": config.get(CONF_HIDE_OPEN_HOME_FOUNDATION, True),
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
        vol.Optional("hide_open_home_foundation"): cv.boolean,
    })
    @websocket_api.require_admin
    @websocket_api.async_response
    async def websocket_update_config(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        """Update rebrand configuration. Requires admin privileges."""
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
        if "hide_open_home_foundation" in msg:
            config[CONF_HIDE_OPEN_HOME_FOUNDATION] = msg["hide_open_home_foundation"]

        hass.data[DOMAIN] = config

        # Write updated config to static JSON file
        await _async_write_config_json(hass)

        connection.send_result(msg["id"], {"success": True})

    websocket_api.async_register_command(hass, websocket_get_config)
    websocket_api.async_register_command(hass, websocket_update_config)


class RebrandConfigView(HomeAssistantView):
    """View to get rebrand configuration via HTTP."""

    url = "/api/ha_rebrand/brand_config"
    name = "api:ha_rebrand:brand_config"
    requires_auth = False  # Allow unauthenticated access for injector script

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self.hass = hass

    async def get(self, request):
        """Handle GET request."""
        config = self.hass.data.get(DOMAIN, {})
        return self.json({
            "brand_name": config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
            "logo": config.get(CONF_LOGO),
            "logo_dark": config.get(CONF_LOGO_DARK),
            "favicon": config.get(CONF_FAVICON),
            "sidebar_title": config.get(CONF_SIDEBAR_TITLE),
            "document_title": config.get(CONF_DOCUMENT_TITLE),
            "replacements": config.get(CONF_REPLACEMENTS, {}),
            "hide_open_home_foundation": config.get(CONF_HIDE_OPEN_HOME_FOUNDATION, True),
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

        # Prepare config for YAML (without top-level domain key for !include)
        yaml_config: dict[str, Any] = {
            CONF_BRAND_NAME: config.get(CONF_BRAND_NAME, DEFAULT_BRAND_NAME),
        }

        if config.get(CONF_LOGO):
            yaml_config[CONF_LOGO] = config[CONF_LOGO]
        if config.get(CONF_LOGO_DARK):
            yaml_config[CONF_LOGO_DARK] = config[CONF_LOGO_DARK]
        if config.get(CONF_FAVICON):
            yaml_config[CONF_FAVICON] = config[CONF_FAVICON]
        if config.get(CONF_SIDEBAR_TITLE):
            yaml_config[CONF_SIDEBAR_TITLE] = config[CONF_SIDEBAR_TITLE]
        if config.get(CONF_DOCUMENT_TITLE):
            yaml_config[CONF_DOCUMENT_TITLE] = config[CONF_DOCUMENT_TITLE]
        if config.get(CONF_REPLACEMENTS):
            yaml_config[CONF_REPLACEMENTS] = config[CONF_REPLACEMENTS]

        # Write to file using executor to avoid blocking
        config_path = self.hass.config.path("ha_rebrand.yaml")
        await self.hass.async_add_executor_job(
            partial(self._write_yaml, config_path, yaml_config)
        )

        return self.json({
            "success": True,
            "path": config_path,
            "message": "Configuration saved. Restart Home Assistant to apply changes.",
        })

    @staticmethod
    def _write_yaml(config_path: str, yaml_config: dict) -> None:
        """Write YAML configuration to file."""
        import yaml
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(yaml_config, f, default_flow_style=False, allow_unicode=True)
