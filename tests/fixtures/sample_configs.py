"""Sample configuration data for HA Rebrand tests.

This module contains valid and invalid configuration samples for testing
the HA Rebrand component's configuration handling and validation.

Usage:
    from tests.fixtures.sample_configs import VALID_CONFIGS, INVALID_CONFIGS
    
    @pytest.mark.parametrize("config", VALID_CONFIGS)
    def test_valid_config_acceptance(config):
        result = validate_config(config)
        assert result.is_valid
"""

from typing import Any

# Default brand name used in tests
DEFAULT_BRAND_NAME = "Home Assistant"

# Valid configuration samples
SAMPLE_CONFIG_DATA: dict[str, Any] = {
    "brand_name": "My Smart Home",
    "logo": "/local/ha_rebrand/logo.png",
    "logo_dark": "/local/ha_rebrand/logo_dark.png",
    "favicon": "/local/ha_rebrand/favicon.ico",
    "sidebar_title": "Smart Home",
    "document_title": "My Home Control",
    "hide_open_home_foundation": True,
    "primary_color": "#3498db",
    "replacements": {
        "Home Assistant": "Smart Home",
        "HA": "SH",
    },
}

# Collection of valid configurations
VALID_CONFIGS: list[dict[str, Any]] = [
    # Minimal valid config (defaults only)
    {},
    
    # Only brand name
    {"brand_name": "Custom Brand"},
    
    # Full configuration
    SAMPLE_CONFIG_DATA.copy(),
    
    # Logo configurations
    {"logo": "/local/custom/logo.png"},
    {"logo": "/local/custom/logo.svg"},
    {"logo": "/local/custom/logo.webp"},
    
    # Light and dark mode logos
    {
        "logo": "/local/ha_rebrand/logo.png",
        "logo_dark": "/local/ha_rebrand/logo_dark.png",
    },
    
    # Favicon only
    {"favicon": "/local/custom/favicon.ico"},
    {"favicon": "/local/custom/favicon.png"},
    
    # Title configurations
    {
        "sidebar_title": "My Home",
        "document_title": "Home Control Panel",
    },
    
    # Color configurations
    {"primary_color": "#FF0000"},
    {"primary_color": "#f00"},
    {"primary_color": "#FF000080"},  # With alpha
    
    # Hide Open Home Foundation
    {"hide_open_home_foundation": True},
    {"hide_open_home_foundation": False},
    
    # Replacements
    {
        "replacements": {
            "Home Assistant": "My Home",
        },
    },
    {
        "replacements": {
            "Home Assistant": "Smart Home",
            "HA": "SH",
            "hass": "home",
        },
    },
    
    # Unicode in values
    {"brand_name": "\u4e2d\u6587\u667a\u80fd\u5bb6\u5c45"},  # Chinese
    {"brand_name": "\u30b9\u30de\u30fc\u30c8\u30db\u30fc\u30e0"},  # Japanese
    
    # Long brand name
    {"brand_name": "A" * 100},
    
    # Special characters in brand name (should be escaped)
    {"brand_name": "Home & Garden"},
    {"brand_name": "Home's Best"},
]

# Invalid configuration samples
INVALID_CONFIGS: list[tuple[dict[str, Any], str]] = [
    # Invalid color formats
    ({"primary_color": "invalid"}, "invalid color format"),
    ({"primary_color": "rgb(255,0,0)"}, "rgb not allowed"),
    ({"primary_color": "#GGG"}, "invalid hex characters"),
    ({"primary_color": "#12345"}, "invalid hex length"),
    ({"primary_color": "red"}, "named colors not allowed"),
    
    # Invalid paths (potential path traversal)
    ({"logo": "../../../etc/passwd"}, "path traversal attempt"),
    ({"logo": "file:///etc/passwd"}, "file protocol not allowed"),
    ({"logo": "http://evil.com/logo.png"}, "external URL not allowed"),
    
    # Empty required values (if required)
    ({"brand_name": ""}, "empty brand name"),
    
    # Wrong types
    ({"brand_name": 123}, "brand_name should be string"),
    ({"hide_open_home_foundation": "true"}, "should be boolean"),
    ({"replacements": "invalid"}, "replacements should be dict"),
]

# Sample color values for testing color validation
SAMPLE_COLOR_VALUES: dict[str, list[str]] = {
    # Valid hex color formats
    "valid_hex_3": [
        "#FFF",
        "#000",
        "#f00",
        "#0F0",
        "#00f",
        "#abc",
    ],
    "valid_hex_6": [
        "#FFFFFF",
        "#000000",
        "#FF0000",
        "#00FF00",
        "#0000FF",
        "#3498db",
        "#e74c3c",
        "#2ecc71",
    ],
    "valid_hex_8": [
        "#FFFFFF00",  # With alpha
        "#00000080",
        "#FF0000FF",
        "#3498db40",
    ],
    
    # Invalid color formats
    "invalid": [
        "",  # Empty
        "red",  # Named color
        "rgb(255, 0, 0)",  # RGB function
        "rgba(255, 0, 0, 0.5)",  # RGBA function
        "hsl(0, 100%, 50%)",  # HSL function
        "#GGG",  # Invalid hex chars
        "#12345",  # Wrong length
        "#1234567890",  # Too long
        "123456",  # Missing #
        "#",  # Just hash
        "##FFFFFF",  # Double hash
        " #FFFFFF",  # Leading space
        "#FFFFFF ",  # Trailing space
    ],
}

# Sample file upload data for testing upload handling
SAMPLE_FILE_UPLOAD_DATA: dict[str, dict[str, Any]] = {
    # Valid file uploads
    "valid_png": {
        "filename": "logo.png",
        "content_type": "image/png",
        "extension": ".png",
        "size": 1024,  # 1KB
        "type": "logo",
    },
    "valid_svg": {
        "filename": "logo.svg",
        "content_type": "image/svg+xml",
        "extension": ".svg",
        "size": 512,
        "type": "logo",
    },
    "valid_jpg": {
        "filename": "background.jpg",
        "content_type": "image/jpeg",
        "extension": ".jpg",
        "size": 2048,
        "type": "logo",
    },
    "valid_ico": {
        "filename": "favicon.ico",
        "content_type": "image/x-icon",
        "extension": ".ico",
        "size": 256,
        "type": "favicon",
    },
    "valid_webp": {
        "filename": "logo.webp",
        "content_type": "image/webp",
        "extension": ".webp",
        "size": 1536,
        "type": "logo",
    },
    
    # Invalid file uploads
    "invalid_extension": {
        "filename": "script.js",
        "content_type": "application/javascript",
        "extension": ".js",
        "size": 100,
        "type": "logo",
        "expected_error": "Invalid file extension",
    },
    "invalid_type": {
        "filename": "data.html",
        "content_type": "text/html",
        "extension": ".html",
        "size": 500,
        "type": "logo",
        "expected_error": "Invalid file extension",
    },
    "too_large": {
        "filename": "huge.png",
        "content_type": "image/png",
        "extension": ".png",
        "size": 10 * 1024 * 1024,  # 10MB - exceeds 5MB limit
        "type": "logo",
        "expected_error": "File too large",
    },
    "invalid_file_type": {
        "filename": "logo.png",
        "content_type": "image/png",
        "extension": ".png",
        "size": 1024,
        "type": "invalid_type",  # Not in ALLOWED_FILE_TYPES
        "expected_error": "Invalid file type",
    },
    "path_traversal": {
        "filename": "../../../etc/passwd",
        "content_type": "image/png",
        "extension": "",
        "size": 100,
        "type": "logo",
        "expected_error": "Invalid filename",
    },
}

# Mock config entry data
MOCK_CONFIG_ENTRY_DATA: dict[str, Any] = {
    "entry_id": "test_entry_id",
    "domain": "ha_rebrand",
    "title": "HA Rebrand",
    "data": {},
    "options": {},
    "unique_id": "ha_rebrand_unique_id",
    "version": 1,
}
