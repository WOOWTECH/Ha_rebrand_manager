"""Test fixtures package for HA Rebrand tests.

This package contains reusable test data and fixtures:
- xss_payloads: XSS attack vectors for security testing
- sample_configs: Valid and invalid configuration samples

Usage:
    from tests.fixtures import XSS_PAYLOADS, SAFE_STRINGS
    from tests.fixtures import VALID_CONFIGS, INVALID_CONFIGS
"""

from tests.fixtures.sample_configs import (
    DEFAULT_BRAND_NAME,
    INVALID_CONFIGS,
    MOCK_CONFIG_ENTRY_DATA,
    SAMPLE_COLOR_VALUES,
    SAMPLE_CONFIG_DATA,
    SAMPLE_FILE_UPLOAD_DATA,
    VALID_CONFIGS,
)
from tests.fixtures.xss_payloads import (
    CSS_INJECTION_PAYLOADS,
    JS_ESCAPE_PAYLOADS,
    SAFE_STRINGS,
    XSS_PAYLOADS,
)

__all__ = [
    # XSS payloads
    "XSS_PAYLOADS",
    "SAFE_STRINGS",
    "CSS_INJECTION_PAYLOADS",
    "JS_ESCAPE_PAYLOADS",
    # Sample configs
    "VALID_CONFIGS",
    "INVALID_CONFIGS",
    "SAMPLE_CONFIG_DATA",
    "SAMPLE_COLOR_VALUES",
    "SAMPLE_FILE_UPLOAD_DATA",
    "DEFAULT_BRAND_NAME",
    "MOCK_CONFIG_ENTRY_DATA",
]
