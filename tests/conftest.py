"""Pytest fixtures for HA Rebrand tests.

This module contains shared fixtures for testing the HA Rebrand custom component.
It provides mock Home Assistant instances, config entries, and test data.

Usage:
    # Fixtures are automatically discovered by pytest
    def test_example(hass, mock_config_entry):
        # hass is a mock HomeAssistant instance
        # mock_config_entry is a MockConfigEntry for ha_rebrand
        pass
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator, Generator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Import test data fixtures
from tests.fixtures.sample_configs import (
    MOCK_CONFIG_ENTRY_DATA,
    SAMPLE_COLOR_VALUES,
    SAMPLE_CONFIG_DATA,
    SAMPLE_FILE_UPLOAD_DATA,
)
from tests.fixtures.xss_payloads import (
    CSS_INJECTION_PAYLOADS,
    JS_ESCAPE_PAYLOADS,
    SAFE_STRINGS,
    XSS_PAYLOADS,
)

# Try to import Home Assistant test utilities
# These may not be available in all environments
try:
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    HAS_HA_TEST_UTILS = True
except ImportError:
    HAS_HA_TEST_UTILS = False
    MockConfigEntry = None

try:
    from homeassistant.core import HomeAssistant

    HAS_HOMEASSISTANT = True
except ImportError:
    HAS_HOMEASSISTANT = False
    HomeAssistant = None


# =============================================================================
# Core Fixtures
# =============================================================================


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock Home Assistant instance for standalone testing.

    This fixture provides a basic mock when the full HA test framework
    is not available. For full integration tests, use the 'hass' fixture
    from pytest-homeassistant-custom-component.

    Returns:
        MagicMock: A mock HomeAssistant instance with common attributes.

    Example:
        def test_something(mock_hass):
            mock_hass.data["my_domain"] = {"key": "value"}
            assert mock_hass.data["my_domain"]["key"] == "value"
    """
    mock = MagicMock()
    mock.data = {}
    mock.config = MagicMock()
    mock.config.path = Mock(side_effect=lambda *args: os.path.join("/config", *args))
    mock.http = MagicMock()
    mock.http.app = MagicMock()
    mock.loop = MagicMock()
    mock.async_add_executor_job = AsyncMock(side_effect=lambda func, *args: func(*args))
    mock.async_create_task = MagicMock()
    mock.bus = MagicMock()
    mock.bus.async_fire = MagicMock()
    mock.services = MagicMock()
    mock.states = MagicMock()
    mock.auth = MagicMock()
    mock.config_entries = MagicMock()
    return mock


@pytest.fixture
def mock_config_entry() -> MockConfigEntry | MagicMock:
    """Create a mock config entry for HA Rebrand.

    Returns:
        MockConfigEntry or MagicMock: A mock config entry with default values.

    Example:
        async def test_setup(hass, mock_config_entry):
            mock_config_entry.add_to_hass(hass)
            await hass.config_entries.async_setup(mock_config_entry.entry_id)
    """
    if HAS_HA_TEST_UTILS and MockConfigEntry is not None:
        return MockConfigEntry(
            domain="ha_rebrand",
            title="HA Rebrand",
            data={},
            options={},
            unique_id="ha_rebrand_test_entry",
            version=1,
        )
    else:
        # Fallback mock when pytest-homeassistant-custom-component is not available
        mock = MagicMock()
        mock.domain = "ha_rebrand"
        mock.title = "HA Rebrand"
        mock.data = {}
        mock.options = {}
        mock.unique_id = "ha_rebrand_test_entry"
        mock.entry_id = "test_entry_id"
        mock.version = 1
        mock.add_to_hass = MagicMock()
        return mock


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock, None, None]:
    """Override async_setup_entry for testing.

    This fixture patches the component's async_setup_entry to prevent
    actual setup during tests that don't need it.

    Yields:
        AsyncMock: The patched async_setup_entry function.

    Example:
        async def test_config_flow(mock_setup_entry):
            # Config flow tests without triggering actual setup
            result = await flow.async_step_user(user_input={})
            assert mock_setup_entry.called
    """
    with patch(
        "ha_rebrand.async_setup_entry",
        return_value=True,
    ) as mock_setup:
        yield mock_setup


# =============================================================================
# Configuration Data Fixtures
# =============================================================================


@pytest.fixture
def sample_config() -> dict[str, Any]:
    """Provide sample configuration data.

    Returns:
        dict: A complete sample configuration for HA Rebrand.

    Example:
        def test_config_validation(sample_config):
            assert sample_config["brand_name"] == "My Smart Home"
    """
    return SAMPLE_CONFIG_DATA.copy()


@pytest.fixture
def sample_config_minimal() -> dict[str, Any]:
    """Provide minimal configuration data.

    Returns:
        dict: A minimal configuration with only brand_name.
    """
    return {"brand_name": "Test Brand"}


@pytest.fixture
def sample_config_with_logo() -> dict[str, Any]:
    """Provide configuration with logo settings.

    Returns:
        dict: Configuration with logo and logo_dark paths.
    """
    return {
        "brand_name": "Test Brand",
        "logo": "/local/ha_rebrand/logo.png",
        "logo_dark": "/local/ha_rebrand/logo_dark.png",
    }


@pytest.fixture
def sample_config_with_colors() -> dict[str, Any]:
    """Provide configuration with color customization.

    Returns:
        dict: Configuration with primary color setting.
    """
    return {
        "brand_name": "Test Brand",
        "primary_color": "#3498db",
    }


# =============================================================================
# Security Test Data Fixtures
# =============================================================================


@pytest.fixture
def xss_payloads() -> list[str]:
    """Provide XSS attack payloads for security testing.

    Returns:
        list[str]: A comprehensive list of XSS test vectors.

    Example:
        @pytest.mark.parametrize("payload", xss_payloads())
        def test_xss_prevention(payload):
            result = sanitize(payload)
            assert "<script>" not in result.lower()
    """
    return XSS_PAYLOADS.copy()


@pytest.fixture
def safe_strings() -> list[str]:
    """Provide safe strings that should pass through validation.

    Returns:
        list[str]: Strings that should not be modified by sanitization.
    """
    return SAFE_STRINGS.copy()


@pytest.fixture
def css_injection_payloads() -> list[str]:
    """Provide CSS injection test payloads.

    Returns:
        list[str]: CSS-based attack vectors for color validation testing.
    """
    return CSS_INJECTION_PAYLOADS.copy()


@pytest.fixture
def js_escape_payloads() -> list[str]:
    """Provide JavaScript escape test payloads.

    Returns:
        list[str]: Strings requiring proper JS escaping.
    """
    return JS_ESCAPE_PAYLOADS.copy()


# =============================================================================
# Color Validation Fixtures
# =============================================================================


@pytest.fixture
def valid_colors() -> list[str]:
    """Provide valid color values for testing.

    Returns:
        list[str]: All valid hex color formats.
    """
    colors: list[str] = []
    for key in ["valid_hex_3", "valid_hex_6", "valid_hex_8"]:
        colors.extend(SAMPLE_COLOR_VALUES.get(key, []))
    return colors


@pytest.fixture
def invalid_colors() -> list[str]:
    """Provide invalid color values for testing.

    Returns:
        list[str]: Invalid color formats that should be rejected.
    """
    return SAMPLE_COLOR_VALUES.get("invalid", []).copy()


# =============================================================================
# File Upload Fixtures
# =============================================================================


@pytest.fixture
def valid_file_uploads() -> list[dict[str, Any]]:
    """Provide valid file upload test data.

    Returns:
        list[dict]: Valid file upload configurations.
    """
    return [
        data
        for key, data in SAMPLE_FILE_UPLOAD_DATA.items()
        if "expected_error" not in data
    ]


@pytest.fixture
def invalid_file_uploads() -> list[dict[str, Any]]:
    """Provide invalid file upload test data.

    Returns:
        list[dict]: Invalid file upload configurations with expected errors.
    """
    return [
        data for key, data in SAMPLE_FILE_UPLOAD_DATA.items() if "expected_error" in data
    ]


@pytest.fixture
def mock_file_upload() -> MagicMock:
    """Create a mock file upload object.

    Returns:
        MagicMock: A mock representing an aiohttp file upload.
    """
    mock_file = MagicMock()
    mock_file.filename = "test_logo.png"
    mock_file.file = MagicMock()
    mock_file.file.read = Mock(return_value=b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    return mock_file


# =============================================================================
# HTTP/Request Mocking Fixtures
# =============================================================================


@pytest.fixture
def mock_request() -> MagicMock:
    """Create a mock HTTP request object.

    Returns:
        MagicMock: A mock aiohttp request with common attributes.
    """
    request = MagicMock()
    request.method = "GET"
    request.path = "/api/ha_rebrand/config"
    request.headers = {"Authorization": "Bearer test_token"}
    request.json = AsyncMock(return_value={})
    request.post = AsyncMock(return_value={})
    return request


@pytest.fixture
def mock_admin_request(mock_request: MagicMock) -> MagicMock:
    """Create a mock HTTP request from an admin user.

    Returns:
        MagicMock: A mock request with admin user context.
    """
    mock_request["hass_user"] = MagicMock()
    mock_request["hass_user"].is_admin = True
    return mock_request


@pytest.fixture
def mock_non_admin_request(mock_request: MagicMock) -> MagicMock:
    """Create a mock HTTP request from a non-admin user.

    Returns:
        MagicMock: A mock request with non-admin user context.
    """
    mock_request["hass_user"] = MagicMock()
    mock_request["hass_user"].is_admin = False
    return mock_request


# =============================================================================
# WebSocket Fixtures
# =============================================================================


@pytest.fixture
def mock_ws_connection() -> MagicMock:
    """Create a mock WebSocket connection.

    Returns:
        MagicMock: A mock WebSocket connection for testing WS commands.
    """
    connection = MagicMock()
    connection.send_result = MagicMock()
    connection.send_error = MagicMock()
    connection.send_message = MagicMock()
    connection.user = MagicMock()
    connection.user.is_admin = True
    return connection


# =============================================================================
# File System Fixtures
# =============================================================================


@pytest.fixture
def mock_uploads_dir(tmp_path) -> str:
    """Create a temporary uploads directory.

    Args:
        tmp_path: pytest's temporary path fixture.

    Returns:
        str: Path to the temporary uploads directory.
    """
    uploads_dir = tmp_path / "www" / "ha_rebrand"
    uploads_dir.mkdir(parents=True)
    return str(uploads_dir)


@pytest.fixture
def mock_frontend_dir(tmp_path) -> str:
    """Create a temporary frontend directory with mock files.

    Args:
        tmp_path: pytest's temporary path fixture.

    Returns:
        str: Path to the temporary frontend directory.
    """
    frontend_dir = tmp_path / "frontend"
    frontend_dir.mkdir(parents=True)
    
    # Create mock frontend files
    (frontend_dir / "ha-rebrand-panel.js").write_text("// Mock panel JS")
    (frontend_dir / "ha-rebrand-injector.js").write_text("// Mock injector JS")
    
    return str(frontend_dir)


# =============================================================================
# Async Test Helpers
# =============================================================================


@pytest.fixture
def mock_async_add_executor_job() -> Generator[AsyncMock, None, None]:
    """Mock async_add_executor_job to run synchronously.

    Yields:
        AsyncMock: A mock that executes the function synchronously.
    """
    async def run_sync(func, *args):
        return func(*args)

    with patch(
        "homeassistant.core.HomeAssistant.async_add_executor_job",
        side_effect=run_sync,
    ) as mock:
        yield mock


# =============================================================================
# Parametrize Helpers
# =============================================================================


def pytest_generate_tests(metafunc):
    """Generate parametrized tests for security fixtures.

    This hook automatically parametrizes tests that use specific fixture names.
    """
    # Parametrize xss_payload tests
    if "xss_payload" in metafunc.fixturenames:
        metafunc.parametrize("xss_payload", XSS_PAYLOADS, ids=lambda x: x[:30])
    
    # Parametrize safe_string tests
    if "safe_string" in metafunc.fixturenames:
        metafunc.parametrize("safe_string", SAFE_STRINGS, ids=lambda x: x[:30] if x else "empty")
    
    # Parametrize valid_color tests
    if "valid_color" in metafunc.fixturenames:
        all_valid = []
        for key in ["valid_hex_3", "valid_hex_6", "valid_hex_8"]:
            all_valid.extend(SAMPLE_COLOR_VALUES.get(key, []))
        metafunc.parametrize("valid_color", all_valid)
    
    # Parametrize invalid_color tests
    if "invalid_color" in metafunc.fixturenames:
        metafunc.parametrize(
            "invalid_color",
            SAMPLE_COLOR_VALUES.get("invalid", []),
            ids=lambda x: x[:20] if x else "empty",
        )
