"""Constants for HA Rebrand integration."""

DOMAIN = "ha_rebrand"

# Configuration keys (new naming - location-based)
CONF_SYSTEM_NAME = "system_name"
CONF_LOGO = "logo"
CONF_LOGO_DARK = "logo_dark"
CONF_FAVICON = "favicon"
CONF_SIDEBAR_TEXT = "sidebar_text"
CONF_BROWSER_TAB_TITLE = "browser_tab_title"
CONF_HIDE_OPEN_HOME_FOUNDATION = "hide_open_home_foundation"
CONF_PRIMARY_COLOR = "primary_color"

# Old configuration keys (for migration compatibility)
CONF_BRAND_NAME_OLD = "brand_name"
CONF_SIDEBAR_TITLE_OLD = "sidebar_title"
CONF_DOCUMENT_TITLE_OLD = "document_title"

# Default values
DEFAULT_SYSTEM_NAME = "Home Assistant"

# Security constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_FILE_TYPES = {"logo", "logo_dark", "favicon"}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp"}

# Panel constants
PANEL_URL_PATH = "ha-rebrand"
PANEL_COMPONENT_NAME = "ha-rebrand-panel"
PANEL_TITLE = "Rebrand"
PANEL_ICON = "mdi:palette-outline"
