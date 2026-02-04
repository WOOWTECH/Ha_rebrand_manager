"""Constants for HA Rebrand integration."""

DOMAIN = "ha_rebrand"

# Configuration keys
CONF_BRAND_NAME = "brand_name"
CONF_LOGO = "logo"
CONF_LOGO_DARK = "logo_dark"
CONF_FAVICON = "favicon"
CONF_SIDEBAR_TITLE = "sidebar_title"
CONF_DOCUMENT_TITLE = "document_title"
CONF_HIDE_OPEN_HOME_FOUNDATION = "hide_open_home_foundation"
CONF_PRIMARY_COLOR = "primary_color"

# Default values
DEFAULT_BRAND_NAME = "Home Assistant"

# Security constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_FILE_TYPES = {"logo", "logo_dark", "favicon"}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp"}

# Panel constants
PANEL_URL_PATH = "ha-rebrand"
PANEL_COMPONENT_NAME = "ha-rebrand-panel"
PANEL_TITLE = "Rebrand"
PANEL_ICON = "mdi:palette-outline"
