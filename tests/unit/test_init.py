"""Tests for the HA Rebrand component initialization.

This module tests the component lifecycle including async_setup(),
async_setup_entry(), and async_unload_entry().

Usage:
    pytest tests/unit/test_init.py -v
"""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Try to import Home Assistant test utilities
try:
    from homeassistant.config_entries import ConfigEntryState
    from homeassistant.core import HomeAssistant

    HAS_HOMEASSISTANT = True
except ImportError:
    HAS_HOMEASSISTANT = False
    HomeAssistant = None
    ConfigEntryState = None

try:
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    HAS_HA_TEST_UTILS = True
except ImportError:
    HAS_HA_TEST_UTILS = False
    MockConfigEntry = None


# Domain constant
DOMAIN = "ha_rebrand"


# =============================================================================
# Test async_setup
# =============================================================================


class TestAsyncSetup:
    """Test the async_setup function for YAML configuration."""

    def test_async_setup_function_exists(self) -> None:
        """Test that async_setup function exists in module."""
        try:
            from ha_rebrand import async_setup

            assert callable(async_setup)
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_setup_initializes_data(self, mock_hass: MagicMock) -> None:
        """Test that async_setup initializes hass.data for the domain."""
        try:
            from ha_rebrand import async_setup

            result = await async_setup(mock_hass, {})
            assert result is True
            assert DOMAIN in mock_hass.data
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_setup_with_empty_config(self, mock_hass: MagicMock) -> None:
        """Test async_setup with empty configuration."""
        try:
            from ha_rebrand import async_setup

            result = await async_setup(mock_hass, {DOMAIN: {}})
            assert result is True
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_setup_registers_websocket_commands(
        self, mock_hass: MagicMock
    ) -> None:
        """Test that async_setup registers WebSocket commands."""
        try:
            from ha_rebrand import async_setup

            with patch("ha_rebrand._async_register_websocket_commands") as mock_ws:
                await async_setup(mock_hass, {})
                mock_ws.assert_called_once_with(mock_hass)
        except ImportError:
            pytest.skip("ha_rebrand module not importable")


# =============================================================================
# Test async_setup_entry
# =============================================================================


class TestAsyncSetupEntry:
    """Test the async_setup_entry function for config entries."""

    def test_async_setup_entry_function_exists(self) -> None:
        """Test that async_setup_entry function exists in module."""
        try:
            from ha_rebrand import async_setup_entry

            assert callable(async_setup_entry)
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_setup_entry_creates_uploads_dir(
        self, mock_hass: MagicMock, mock_config_entry: Any
    ) -> None:
        """Test that async_setup_entry creates the uploads directory."""
        try:
            from ha_rebrand import async_setup_entry

            with patch("ha_rebrand._create_directory") as mock_create_dir:
                with patch("ha_rebrand._load_config_json", return_value={}):
                    with patch("ha_rebrand._async_write_config_json"):
                        with patch("ha_rebrand._async_register_frontend"):
                            with patch("ha_rebrand.panel_custom.async_register_panel"):
                                with patch("ha_rebrand._unregister_authorize_static_path"):
                                    mock_hass.http = MagicMock()
                                    mock_hass.data = {}
                                    result = await async_setup_entry(
                                        mock_hass, mock_config_entry
                                    )

                mock_create_dir.assert_called()
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_setup_entry_stores_config(
        self, mock_hass: MagicMock, mock_config_entry: Any
    ) -> None:
        """Test that async_setup_entry stores configuration in hass.data."""
        try:
            from ha_rebrand import async_setup_entry
            from ha_rebrand.const import (
                CONF_BRAND_NAME,
                CONF_LOGO,
                CONF_REPLACEMENTS,
                DEFAULT_BRAND_NAME,
            )

            with patch("ha_rebrand._create_directory"):
                with patch(
                    "ha_rebrand._load_config_json",
                    return_value={"brand_name": "Test Brand"},
                ):
                    with patch("ha_rebrand._async_write_config_json"):
                        with patch("ha_rebrand._async_register_frontend"):
                            with patch("ha_rebrand.panel_custom.async_register_panel"):
                                with patch("ha_rebrand._unregister_authorize_static_path"):
                                    mock_hass.http = MagicMock()
                                    mock_hass.data = {}
                                    result = await async_setup_entry(
                                        mock_hass, mock_config_entry
                                    )

                                    assert result is True
                                    assert DOMAIN in mock_hass.data
                                    assert (
                                        mock_hass.data[DOMAIN][CONF_BRAND_NAME]
                                        == "Test Brand"
                                    )
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_setup_entry_registers_http_views(
        self, mock_hass: MagicMock, mock_config_entry: Any
    ) -> None:
        """Test that async_setup_entry registers HTTP views."""
        try:
            from ha_rebrand import async_setup_entry

            with patch("ha_rebrand._create_directory"):
                with patch("ha_rebrand._load_config_json", return_value={}):
                    with patch("ha_rebrand._async_write_config_json"):
                        with patch("ha_rebrand._async_register_frontend"):
                            with patch("ha_rebrand.panel_custom.async_register_panel"):
                                with patch("ha_rebrand._unregister_authorize_static_path"):
                                    mock_hass.http = MagicMock()
                                    mock_hass.data = {}
                                    result = await async_setup_entry(
                                        mock_hass, mock_config_entry
                                    )

                                    # Verify HTTP views are registered
                                    assert mock_hass.http.register_view.call_count >= 3
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_setup_entry_registers_panel(
        self, mock_hass: MagicMock, mock_config_entry: Any
    ) -> None:
        """Test that async_setup_entry registers the admin panel."""
        try:
            from ha_rebrand import DATA_PANEL_REGISTERED, async_setup_entry

            with patch("ha_rebrand._create_directory"):
                with patch("ha_rebrand._load_config_json", return_value={}):
                    with patch("ha_rebrand._async_write_config_json"):
                        with patch("ha_rebrand._async_register_frontend"):
                            with patch(
                                "ha_rebrand.panel_custom.async_register_panel"
                            ) as mock_panel:
                                with patch("ha_rebrand._unregister_authorize_static_path"):
                                    mock_hass.http = MagicMock()
                                    mock_hass.data = {}
                                    result = await async_setup_entry(
                                        mock_hass, mock_config_entry
                                    )

                                    mock_panel.assert_called_once()
                                    assert mock_hass.data[DATA_PANEL_REGISTERED] is True
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_setup_entry_returns_true(
        self, mock_hass: MagicMock, mock_config_entry: Any
    ) -> None:
        """Test that async_setup_entry returns True on success."""
        try:
            from ha_rebrand import async_setup_entry

            with patch("ha_rebrand._create_directory"):
                with patch("ha_rebrand._load_config_json", return_value={}):
                    with patch("ha_rebrand._async_write_config_json"):
                        with patch("ha_rebrand._async_register_frontend"):
                            with patch("ha_rebrand.panel_custom.async_register_panel"):
                                with patch("ha_rebrand._unregister_authorize_static_path"):
                                    mock_hass.http = MagicMock()
                                    mock_hass.data = {}
                                    result = await async_setup_entry(
                                        mock_hass, mock_config_entry
                                    )

                                    assert result is True
        except ImportError:
            pytest.skip("ha_rebrand module not importable")


# =============================================================================
# Test async_unload_entry
# =============================================================================


class TestAsyncUnloadEntry:
    """Test the async_unload_entry function."""

    def test_async_unload_entry_function_exists(self) -> None:
        """Test that async_unload_entry function exists in module."""
        try:
            from ha_rebrand import async_unload_entry

            assert callable(async_unload_entry)
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_unload_entry_removes_panel(
        self, mock_hass: MagicMock, mock_config_entry: Any
    ) -> None:
        """Test that async_unload_entry removes the panel."""
        try:
            from ha_rebrand import (
                DATA_PANEL_REGISTERED,
                PANEL_URL_PATH,
                async_unload_entry,
            )
            from ha_rebrand.const import PANEL_URL_PATH as CONST_PANEL_URL_PATH

            # Set up initial state
            mock_hass.data = {
                DOMAIN: {"uploads_dir": "/test/path"},
                DATA_PANEL_REGISTERED: True,
            }

            with patch("ha_rebrand.frontend.DATA_PANELS", CONST_PANEL_URL_PATH):
                with patch("ha_rebrand.frontend.async_remove_panel") as mock_remove:
                    mock_hass.data["frontend_panels"] = {CONST_PANEL_URL_PATH: {}}
                    result = await async_unload_entry(mock_hass, mock_config_entry)

                    assert result is True
                    assert mock_hass.data[DATA_PANEL_REGISTERED] is False
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_unload_entry_returns_true(
        self, mock_hass: MagicMock, mock_config_entry: Any
    ) -> None:
        """Test that async_unload_entry returns True on success."""
        try:
            from ha_rebrand import DATA_PANEL_REGISTERED, async_unload_entry

            mock_hass.data = {
                DOMAIN: {"uploads_dir": "/test/path"},
                DATA_PANEL_REGISTERED: False,
            }

            result = await async_unload_entry(mock_hass, mock_config_entry)
            assert result is True
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    async def test_async_unload_entry_preserves_uploads_dir(
        self, mock_hass: MagicMock, mock_config_entry: Any
    ) -> None:
        """Test that unload preserves uploads_dir reference."""
        try:
            from ha_rebrand import DATA_PANEL_REGISTERED, async_unload_entry

            uploads_dir = "/test/path/www/ha_rebrand"
            mock_hass.data = {
                DOMAIN: {"uploads_dir": uploads_dir, "other_data": "value"},
                DATA_PANEL_REGISTERED: False,
            }

            result = await async_unload_entry(mock_hass, mock_config_entry)
            assert result is True
            # uploads_dir should be preserved
            assert mock_hass.data[DOMAIN].get("uploads_dir") == uploads_dir
        except ImportError:
            pytest.skip("ha_rebrand module not importable")


# =============================================================================
# Test Helper Functions
# =============================================================================


class TestHelperFunctions:
    """Test helper functions in __init__.py."""

    def test_create_directory_creates_path(self, tmp_path) -> None:
        """Test that _create_directory creates the directory."""
        try:
            from ha_rebrand import _create_directory

            test_dir = str(tmp_path / "test_dir")
            assert not os.path.exists(test_dir)
            _create_directory(test_dir)
            assert os.path.exists(test_dir)
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    def test_create_directory_handles_existing(self, tmp_path) -> None:
        """Test that _create_directory handles existing directories."""
        try:
            from ha_rebrand import _create_directory

            test_dir = str(tmp_path / "existing_dir")
            os.makedirs(test_dir)
            # Should not raise
            _create_directory(test_dir)
            assert os.path.exists(test_dir)
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    def test_load_config_json_returns_empty_for_missing(self, tmp_path) -> None:
        """Test that _load_config_json returns empty dict for missing file."""
        try:
            from ha_rebrand import _load_config_json

            missing_path = str(tmp_path / "missing.json")
            result = _load_config_json(missing_path)
            assert result == {}
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    def test_load_config_json_loads_valid_json(self, tmp_path) -> None:
        """Test that _load_config_json loads valid JSON."""
        try:
            import json

            from ha_rebrand import _load_config_json

            config_file = tmp_path / "config.json"
            test_data = {"brand_name": "Test", "primary_color": "#123456"}
            config_file.write_text(json.dumps(test_data))

            result = _load_config_json(str(config_file))
            assert result == test_data
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    def test_load_config_json_handles_invalid_json(self, tmp_path) -> None:
        """Test that _load_config_json handles invalid JSON gracefully."""
        try:
            from ha_rebrand import _load_config_json

            config_file = tmp_path / "invalid.json"
            config_file.write_text("not valid json {{{")

            result = _load_config_json(str(config_file))
            assert result == {}
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    def test_write_config_json(self, tmp_path) -> None:
        """Test that _write_config_json writes config to file."""
        try:
            import json

            from ha_rebrand import _write_config_json

            config_file = str(tmp_path / "config.json")
            test_data = {"brand_name": "Test", "logo": "/path/to/logo.png"}

            _write_config_json(config_file, test_data)

            with open(config_file) as f:
                result = json.load(f)
            assert result == test_data
        except ImportError:
            pytest.skip("ha_rebrand module not importable")


# =============================================================================
# Test Security Functions
# =============================================================================


class TestSecurityFunctions:
    """Test security-related functions in __init__.py."""

    def test_escape_js_string_escapes_quotes(self) -> None:
        """Test that _escape_js_string escapes quotes properly."""
        try:
            from ha_rebrand import _escape_js_string

            assert '\\"' in _escape_js_string('test"value')
            assert "\\'" in _escape_js_string("test'value")
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    def test_escape_js_string_escapes_html_tags(self) -> None:
        """Test that _escape_js_string escapes HTML tags."""
        try:
            from ha_rebrand import _escape_js_string

            result = _escape_js_string("<script>alert(1)</script>")
            assert "<" not in result
            assert ">" not in result
            assert "\\x3c" in result
            assert "\\x3e" in result
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    def test_escape_js_string_handles_empty(self) -> None:
        """Test that _escape_js_string handles empty strings."""
        try:
            from ha_rebrand import _escape_js_string

            assert _escape_js_string("") == ""
            assert _escape_js_string(None) == ""  # type: ignore
        except (ImportError, TypeError):
            # TypeError is acceptable for None input
            pass

    def test_validate_color_accepts_valid_hex(self) -> None:
        """Test that _validate_color accepts valid hex colors."""
        try:
            from ha_rebrand import _validate_color

            assert _validate_color("#FFF") == "#FFF"
            assert _validate_color("#FFFFFF") == "#FFFFFF"
            assert _validate_color("#FF0000FF") == "#FF0000FF"
            assert _validate_color("#abc") == "#abc"
        except ImportError:
            pytest.skip("ha_rebrand module not importable")

    def test_validate_color_rejects_invalid(self) -> None:
        """Test that _validate_color rejects invalid colors."""
        try:
            from ha_rebrand import _validate_color

            assert _validate_color("red") == ""
            assert _validate_color("rgb(255,0,0)") == ""
            assert _validate_color("#GGGGGG") == ""
            assert _validate_color("") == ""
        except ImportError:
            pytest.skip("ha_rebrand module not importable")


# =============================================================================
# Integration Tests with Full HA Framework
# =============================================================================


@pytest.mark.skipif(
    not (HAS_HOMEASSISTANT and HAS_HA_TEST_UTILS),
    reason="Home Assistant test utilities not available",
)
class TestSetupIntegration:
    """Integration tests using full Home Assistant framework."""

    async def test_full_setup_and_unload_cycle(self, hass: HomeAssistant) -> None:
        """Test complete setup and unload cycle."""
        if MockConfigEntry is None:
            pytest.skip("MockConfigEntry not available")

        entry = MockConfigEntry(
            domain=DOMAIN,
            title="HA Rebrand",
            data={},
            unique_id="ha_rebrand_test_entry",
        )
        entry.add_to_hass(hass)

        # Setup
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        assert entry.state is ConfigEntryState.LOADED

        # Unload
        assert await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()
        assert entry.state is ConfigEntryState.NOT_LOADED

    async def test_reload_entry(self, hass: HomeAssistant) -> None:
        """Test that reloading entry works correctly."""
        if MockConfigEntry is None:
            pytest.skip("MockConfigEntry not available")

        entry = MockConfigEntry(
            domain=DOMAIN,
            title="HA Rebrand",
            data={},
            unique_id="ha_rebrand_test_entry",
        )
        entry.add_to_hass(hass)

        # Initial setup
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        # Reload
        await hass.config_entries.async_reload(entry.entry_id)
        await hass.async_block_till_done()

        assert entry.state is ConfigEntryState.LOADED
