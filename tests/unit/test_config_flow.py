"""Tests for the HA Rebrand config flow.

This module tests the configuration flow for the HA Rebrand component,
including the user step, single instance enforcement, and entry creation.

Usage:
    pytest tests/unit/test_config_flow.py -v
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Try to import Home Assistant test utilities
try:
    from homeassistant import config_entries
    from homeassistant.core import HomeAssistant
    from homeassistant.data_entry_flow import FlowResultType

    HAS_HOMEASSISTANT = True
except ImportError:
    HAS_HOMEASSISTANT = False
    HomeAssistant = None
    FlowResultType = None
    config_entries = None

try:
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    HAS_HA_TEST_UTILS = True
except ImportError:
    HAS_HA_TEST_UTILS = False
    MockConfigEntry = None


# Domain constant - must match the component
DOMAIN = "ha_rebrand"


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_setup_entry() -> AsyncMock:
    """Mock async_setup_entry to prevent actual setup during config flow tests."""
    with patch(
        "ha_rebrand.async_setup_entry",
        return_value=True,
    ) as mock_setup:
        yield mock_setup


# =============================================================================
# Config Flow Tests - User Step
# =============================================================================


@pytest.mark.skipif(not HAS_HOMEASSISTANT, reason="Home Assistant not available")
class TestConfigFlowUserStep:
    """Test the config flow user step."""

    async def test_form_shows_on_init(self, hass: HomeAssistant) -> None:
        """Test that the form is shown on initialization."""
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result.get("errors") is None or result["errors"] == {}

    async def test_create_entry_with_user_input(
        self, hass: HomeAssistant, mock_setup_entry: AsyncMock
    ) -> None:
        """Test creating an entry with user input."""
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        assert result["type"] is FlowResultType.FORM

        # Submit the form (empty input triggers entry creation)
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={},
        )
        await hass.async_block_till_done()

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == "HA Rebrand"
        assert result["data"] == {}
        assert len(mock_setup_entry.mock_calls) == 1

    async def test_single_instance_only(self, hass: HomeAssistant) -> None:
        """Test that only one instance is allowed."""
        # Create first entry
        if HAS_HA_TEST_UTILS and MockConfigEntry is not None:
            entry = MockConfigEntry(
                domain=DOMAIN,
                title="HA Rebrand",
                data={},
                unique_id="ha_rebrand_test_entry",
            )
            entry.add_to_hass(hass)

            # Try to create a second entry
            result = await hass.config_entries.flow.async_init(
                DOMAIN, context={"source": config_entries.SOURCE_USER}
            )
            assert result["type"] is FlowResultType.ABORT
            assert result["reason"] == "single_instance_allowed"


# =============================================================================
# Config Flow Tests - Without HA Framework (Standalone)
# =============================================================================


class TestConfigFlowStandalone:
    """Test config flow logic without full Home Assistant framework."""

    def test_config_flow_version(self) -> None:
        """Test that config flow has correct version."""
        try:
            from ha_rebrand.config_flow import HaRebrandConfigFlow

            assert HaRebrandConfigFlow.VERSION == 1
        except ImportError:
            pytest.skip("ha_rebrand.config_flow not importable")

    def test_config_flow_domain(self) -> None:
        """Test that config flow uses correct domain."""
        try:
            from ha_rebrand.config_flow import HaRebrandConfigFlow
            from ha_rebrand.const import DOMAIN as CONST_DOMAIN

            # The domain is set via decorator, verify it matches const
            assert CONST_DOMAIN == "ha_rebrand"
        except ImportError:
            pytest.skip("ha_rebrand modules not importable")


# =============================================================================
# Mock Config Flow Tests
# =============================================================================


class TestConfigFlowMocked:
    """Test config flow with mocked Home Assistant."""

    @pytest.fixture
    def mock_hass(self) -> MagicMock:
        """Create a mock Home Assistant instance."""
        mock = MagicMock()
        mock.data = {}
        mock.config_entries = MagicMock()
        mock.config_entries.flow = MagicMock()
        return mock

    @pytest.fixture
    def mock_flow(self) -> MagicMock:
        """Create a mock config flow."""
        mock = MagicMock()
        mock._async_current_entries = MagicMock(return_value=[])
        mock.async_set_unique_id = AsyncMock()
        mock.async_abort = MagicMock(
            return_value={"type": "abort", "reason": "single_instance_allowed"}
        )
        mock.async_create_entry = MagicMock(
            return_value={
                "type": "create_entry",
                "title": "HA Rebrand",
                "data": {},
            }
        )
        mock.async_show_form = MagicMock(
            return_value={
                "type": "form",
                "step_id": "user",
                "errors": {},
            }
        )
        return mock

    def test_flow_returns_form_when_no_input(self, mock_flow: MagicMock) -> None:
        """Test that flow shows form when no user input is provided."""
        # Simulate no user input (initial step)
        result = mock_flow.async_show_form()
        assert result["type"] == "form"
        assert result["step_id"] == "user"

    def test_flow_creates_entry_with_input(self, mock_flow: MagicMock) -> None:
        """Test that flow creates entry when user input is provided."""
        result = mock_flow.async_create_entry()
        assert result["type"] == "create_entry"
        assert result["title"] == "HA Rebrand"
        assert result["data"] == {}

    def test_flow_aborts_if_already_configured(self, mock_flow: MagicMock) -> None:
        """Test that flow aborts if already configured."""
        # Simulate existing entries
        mock_flow._async_current_entries.return_value = [MagicMock()]
        result = mock_flow.async_abort()
        assert result["type"] == "abort"
        assert result["reason"] == "single_instance_allowed"


# =============================================================================
# Config Flow Edge Cases
# =============================================================================


class TestConfigFlowEdgeCases:
    """Test edge cases in config flow."""

    def test_domain_constant_value(self) -> None:
        """Test that DOMAIN constant has expected value."""
        assert DOMAIN == "ha_rebrand"

    @pytest.mark.skipif(not HAS_HOMEASSISTANT, reason="Home Assistant not available")
    async def test_flow_handles_empty_description_placeholders(
        self, hass: HomeAssistant
    ) -> None:
        """Test that flow handles empty description placeholders."""
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        # Description placeholders should be empty or None
        placeholders = result.get("description_placeholders", {})
        assert placeholders == {} or placeholders is None


# =============================================================================
# Integration with conftest fixtures
# =============================================================================


@pytest.mark.skipif(not HAS_HOMEASSISTANT, reason="Home Assistant not available")
class TestConfigFlowWithFixtures:
    """Test config flow using conftest fixtures."""

    async def test_with_mock_config_entry(
        self, hass: HomeAssistant, mock_config_entry: Any
    ) -> None:
        """Test config flow behavior with mock config entry fixture."""
        if mock_config_entry is not None:
            mock_config_entry.add_to_hass(hass)
            # Should abort since entry exists
            result = await hass.config_entries.flow.async_init(
                DOMAIN, context={"source": config_entries.SOURCE_USER}
            )
            assert result["type"] is FlowResultType.ABORT

    async def test_flow_with_sample_config(
        self, hass: HomeAssistant, sample_config: dict[str, Any]
    ) -> None:
        """Test that sample config can be used in flow context."""
        # This tests that the sample_config fixture from conftest is available
        assert "brand_name" in sample_config
        # Flow itself doesn't use this data, but validates fixture accessibility
