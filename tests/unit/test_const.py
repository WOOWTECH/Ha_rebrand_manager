"""Tests for the HA Rebrand constants module.

This module tests that all required constants are defined with expected
values and types in the const.py file.

Usage:
    pytest tests/unit/test_const.py -v
"""

from __future__ import annotations

import pytest


# =============================================================================
# Test Domain Constant
# =============================================================================


class TestDomainConstant:
    """Test the DOMAIN constant."""

    def test_domain_exists(self) -> None:
        """Test that DOMAIN constant is defined."""
        try:
            from ha_rebrand.const import DOMAIN

            assert DOMAIN is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_domain_value(self) -> None:
        """Test that DOMAIN has expected value."""
        try:
            from ha_rebrand.const import DOMAIN

            assert DOMAIN == "ha_rebrand"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_domain_is_string(self) -> None:
        """Test that DOMAIN is a string."""
        try:
            from ha_rebrand.const import DOMAIN

            assert isinstance(DOMAIN, str)
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")


# =============================================================================
# Test Configuration Key Constants
# =============================================================================


class TestConfigurationKeys:
    """Test configuration key constants."""

    def test_conf_brand_name_exists(self) -> None:
        """Test that CONF_BRAND_NAME is defined."""
        try:
            from ha_rebrand.const import CONF_BRAND_NAME

            assert CONF_BRAND_NAME == "brand_name"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_conf_logo_exists(self) -> None:
        """Test that CONF_LOGO is defined."""
        try:
            from ha_rebrand.const import CONF_LOGO

            assert CONF_LOGO == "logo"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_conf_logo_dark_exists(self) -> None:
        """Test that CONF_LOGO_DARK is defined."""
        try:
            from ha_rebrand.const import CONF_LOGO_DARK

            assert CONF_LOGO_DARK == "logo_dark"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_conf_favicon_exists(self) -> None:
        """Test that CONF_FAVICON is defined."""
        try:
            from ha_rebrand.const import CONF_FAVICON

            assert CONF_FAVICON == "favicon"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_conf_replacements_exists(self) -> None:
        """Test that CONF_REPLACEMENTS is defined."""
        try:
            from ha_rebrand.const import CONF_REPLACEMENTS

            assert CONF_REPLACEMENTS == "replacements"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_conf_sidebar_title_exists(self) -> None:
        """Test that CONF_SIDEBAR_TITLE is defined."""
        try:
            from ha_rebrand.const import CONF_SIDEBAR_TITLE

            assert CONF_SIDEBAR_TITLE == "sidebar_title"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_conf_document_title_exists(self) -> None:
        """Test that CONF_DOCUMENT_TITLE is defined."""
        try:
            from ha_rebrand.const import CONF_DOCUMENT_TITLE

            assert CONF_DOCUMENT_TITLE == "document_title"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_conf_hide_open_home_foundation_exists(self) -> None:
        """Test that CONF_HIDE_OPEN_HOME_FOUNDATION is defined."""
        try:
            from ha_rebrand.const import CONF_HIDE_OPEN_HOME_FOUNDATION

            assert CONF_HIDE_OPEN_HOME_FOUNDATION == "hide_open_home_foundation"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_conf_primary_color_exists(self) -> None:
        """Test that CONF_PRIMARY_COLOR is defined."""
        try:
            from ha_rebrand.const import CONF_PRIMARY_COLOR

            assert CONF_PRIMARY_COLOR == "primary_color"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_all_conf_keys_are_strings(self) -> None:
        """Test that all CONF_* constants are strings."""
        try:
            from ha_rebrand.const import (
                CONF_BRAND_NAME,
                CONF_DOCUMENT_TITLE,
                CONF_FAVICON,
                CONF_HIDE_OPEN_HOME_FOUNDATION,
                CONF_LOGO,
                CONF_LOGO_DARK,
                CONF_PRIMARY_COLOR,
                CONF_REPLACEMENTS,
                CONF_SIDEBAR_TITLE,
            )

            conf_keys = [
                CONF_BRAND_NAME,
                CONF_LOGO,
                CONF_LOGO_DARK,
                CONF_FAVICON,
                CONF_REPLACEMENTS,
                CONF_SIDEBAR_TITLE,
                CONF_DOCUMENT_TITLE,
                CONF_HIDE_OPEN_HOME_FOUNDATION,
                CONF_PRIMARY_COLOR,
            ]
            for key in conf_keys:
                assert isinstance(key, str), f"{key} is not a string"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")


# =============================================================================
# Test Default Values
# =============================================================================


class TestDefaultValues:
    """Test default value constants."""

    def test_default_brand_name_exists(self) -> None:
        """Test that DEFAULT_BRAND_NAME is defined."""
        try:
            from ha_rebrand.const import DEFAULT_BRAND_NAME

            assert DEFAULT_BRAND_NAME is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_default_brand_name_value(self) -> None:
        """Test that DEFAULT_BRAND_NAME has expected value."""
        try:
            from ha_rebrand.const import DEFAULT_BRAND_NAME

            assert DEFAULT_BRAND_NAME == "Home Assistant"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_default_replacements_exists(self) -> None:
        """Test that DEFAULT_REPLACEMENTS is defined."""
        try:
            from ha_rebrand.const import DEFAULT_REPLACEMENTS

            assert DEFAULT_REPLACEMENTS is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_default_replacements_is_dict(self) -> None:
        """Test that DEFAULT_REPLACEMENTS is a dictionary."""
        try:
            from ha_rebrand.const import DEFAULT_REPLACEMENTS

            assert isinstance(DEFAULT_REPLACEMENTS, dict)
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_default_replacements_is_empty(self) -> None:
        """Test that DEFAULT_REPLACEMENTS is an empty dict by default."""
        try:
            from ha_rebrand.const import DEFAULT_REPLACEMENTS

            assert DEFAULT_REPLACEMENTS == {}
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")


# =============================================================================
# Test Security Constants
# =============================================================================


class TestSecurityConstants:
    """Test security-related constants."""

    def test_max_file_size_exists(self) -> None:
        """Test that MAX_FILE_SIZE is defined."""
        try:
            from ha_rebrand.const import MAX_FILE_SIZE

            assert MAX_FILE_SIZE is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_max_file_size_value(self) -> None:
        """Test that MAX_FILE_SIZE is 5MB."""
        try:
            from ha_rebrand.const import MAX_FILE_SIZE

            # 5MB = 5 * 1024 * 1024 bytes
            assert MAX_FILE_SIZE == 5 * 1024 * 1024
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_max_file_size_is_int(self) -> None:
        """Test that MAX_FILE_SIZE is an integer."""
        try:
            from ha_rebrand.const import MAX_FILE_SIZE

            assert isinstance(MAX_FILE_SIZE, int)
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_allowed_file_types_exists(self) -> None:
        """Test that ALLOWED_FILE_TYPES is defined."""
        try:
            from ha_rebrand.const import ALLOWED_FILE_TYPES

            assert ALLOWED_FILE_TYPES is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_allowed_file_types_is_set(self) -> None:
        """Test that ALLOWED_FILE_TYPES is a set."""
        try:
            from ha_rebrand.const import ALLOWED_FILE_TYPES

            assert isinstance(ALLOWED_FILE_TYPES, set)
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_allowed_file_types_contains_logo(self) -> None:
        """Test that ALLOWED_FILE_TYPES contains 'logo'."""
        try:
            from ha_rebrand.const import ALLOWED_FILE_TYPES

            assert "logo" in ALLOWED_FILE_TYPES
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_allowed_file_types_contains_logo_dark(self) -> None:
        """Test that ALLOWED_FILE_TYPES contains 'logo_dark'."""
        try:
            from ha_rebrand.const import ALLOWED_FILE_TYPES

            assert "logo_dark" in ALLOWED_FILE_TYPES
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_allowed_file_types_contains_favicon(self) -> None:
        """Test that ALLOWED_FILE_TYPES contains 'favicon'."""
        try:
            from ha_rebrand.const import ALLOWED_FILE_TYPES

            assert "favicon" in ALLOWED_FILE_TYPES
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_allowed_extensions_exists(self) -> None:
        """Test that ALLOWED_EXTENSIONS is defined."""
        try:
            from ha_rebrand.const import ALLOWED_EXTENSIONS

            assert ALLOWED_EXTENSIONS is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_allowed_extensions_is_set(self) -> None:
        """Test that ALLOWED_EXTENSIONS is a set."""
        try:
            from ha_rebrand.const import ALLOWED_EXTENSIONS

            assert isinstance(ALLOWED_EXTENSIONS, set)
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_allowed_extensions_contains_expected(self) -> None:
        """Test that ALLOWED_EXTENSIONS contains expected image extensions."""
        try:
            from ha_rebrand.const import ALLOWED_EXTENSIONS

            expected = {".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp"}
            assert expected.issubset(ALLOWED_EXTENSIONS)
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_allowed_extensions_no_dangerous(self) -> None:
        """Test that ALLOWED_EXTENSIONS does not contain dangerous extensions."""
        try:
            from ha_rebrand.const import ALLOWED_EXTENSIONS

            dangerous = {".js", ".html", ".php", ".py", ".sh", ".exe", ".bat"}
            for ext in dangerous:
                assert ext not in ALLOWED_EXTENSIONS, f"Dangerous extension {ext} found"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")


# =============================================================================
# Test Panel Constants
# =============================================================================


class TestPanelConstants:
    """Test panel-related constants."""

    def test_panel_url_path_exists(self) -> None:
        """Test that PANEL_URL_PATH is defined."""
        try:
            from ha_rebrand.const import PANEL_URL_PATH

            assert PANEL_URL_PATH is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_panel_url_path_value(self) -> None:
        """Test that PANEL_URL_PATH has expected value."""
        try:
            from ha_rebrand.const import PANEL_URL_PATH

            assert PANEL_URL_PATH == "ha-rebrand"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_panel_component_name_exists(self) -> None:
        """Test that PANEL_COMPONENT_NAME is defined."""
        try:
            from ha_rebrand.const import PANEL_COMPONENT_NAME

            assert PANEL_COMPONENT_NAME is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_panel_component_name_value(self) -> None:
        """Test that PANEL_COMPONENT_NAME has expected value."""
        try:
            from ha_rebrand.const import PANEL_COMPONENT_NAME

            assert PANEL_COMPONENT_NAME == "ha-rebrand-panel"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_panel_title_exists(self) -> None:
        """Test that PANEL_TITLE is defined."""
        try:
            from ha_rebrand.const import PANEL_TITLE

            assert PANEL_TITLE is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_panel_title_value(self) -> None:
        """Test that PANEL_TITLE has expected value."""
        try:
            from ha_rebrand.const import PANEL_TITLE

            assert PANEL_TITLE == "Rebrand"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_panel_icon_exists(self) -> None:
        """Test that PANEL_ICON is defined."""
        try:
            from ha_rebrand.const import PANEL_ICON

            assert PANEL_ICON is not None
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_panel_icon_is_mdi(self) -> None:
        """Test that PANEL_ICON starts with 'mdi:'."""
        try:
            from ha_rebrand.const import PANEL_ICON

            assert PANEL_ICON.startswith("mdi:")
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_panel_icon_value(self) -> None:
        """Test that PANEL_ICON has expected value."""
        try:
            from ha_rebrand.const import PANEL_ICON

            assert PANEL_ICON == "mdi:palette-outline"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")


# =============================================================================
# Test All Constants Present
# =============================================================================


class TestAllConstantsPresent:
    """Test that all expected constants are present."""

    def test_all_required_constants_importable(self) -> None:
        """Test that all required constants can be imported."""
        try:
            from ha_rebrand.const import (
                ALLOWED_EXTENSIONS,
                ALLOWED_FILE_TYPES,
                CONF_BRAND_NAME,
                CONF_DOCUMENT_TITLE,
                CONF_FAVICON,
                CONF_HIDE_OPEN_HOME_FOUNDATION,
                CONF_LOGO,
                CONF_LOGO_DARK,
                CONF_PRIMARY_COLOR,
                CONF_REPLACEMENTS,
                CONF_SIDEBAR_TITLE,
                DEFAULT_BRAND_NAME,
                DEFAULT_REPLACEMENTS,
                DOMAIN,
                MAX_FILE_SIZE,
                PANEL_COMPONENT_NAME,
                PANEL_ICON,
                PANEL_TITLE,
                PANEL_URL_PATH,
            )

            # If we get here, all imports succeeded
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import constants: {e}")

    def test_constants_count(self) -> None:
        """Test that the expected number of constants are defined."""
        try:
            import ha_rebrand.const as const_module

            # Get all uppercase constants (convention for constants)
            constants = [
                name
                for name in dir(const_module)
                if name.isupper() and not name.startswith("_")
            ]

            # Should have at least 19 constants
            assert len(constants) >= 19, f"Expected at least 19 constants, got {len(constants)}: {constants}"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")


# =============================================================================
# Test Constant Types
# =============================================================================


class TestConstantTypes:
    """Test that constants have correct types."""

    def test_string_constants_are_strings(self) -> None:
        """Test that string constants are strings."""
        try:
            from ha_rebrand.const import (
                CONF_BRAND_NAME,
                CONF_DOCUMENT_TITLE,
                CONF_FAVICON,
                CONF_HIDE_OPEN_HOME_FOUNDATION,
                CONF_LOGO,
                CONF_LOGO_DARK,
                CONF_PRIMARY_COLOR,
                CONF_REPLACEMENTS,
                CONF_SIDEBAR_TITLE,
                DEFAULT_BRAND_NAME,
                DOMAIN,
                PANEL_COMPONENT_NAME,
                PANEL_ICON,
                PANEL_TITLE,
                PANEL_URL_PATH,
            )

            string_constants = [
                DOMAIN,
                CONF_BRAND_NAME,
                CONF_LOGO,
                CONF_LOGO_DARK,
                CONF_FAVICON,
                CONF_REPLACEMENTS,
                CONF_SIDEBAR_TITLE,
                CONF_DOCUMENT_TITLE,
                CONF_HIDE_OPEN_HOME_FOUNDATION,
                CONF_PRIMARY_COLOR,
                DEFAULT_BRAND_NAME,
                PANEL_URL_PATH,
                PANEL_COMPONENT_NAME,
                PANEL_TITLE,
                PANEL_ICON,
            ]

            for const in string_constants:
                assert isinstance(const, str), f"Constant {const} is not a string"
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_numeric_constants_are_numeric(self) -> None:
        """Test that numeric constants are numeric."""
        try:
            from ha_rebrand.const import MAX_FILE_SIZE

            assert isinstance(MAX_FILE_SIZE, (int, float))
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")

    def test_collection_constants_are_collections(self) -> None:
        """Test that collection constants are collections."""
        try:
            from ha_rebrand.const import (
                ALLOWED_EXTENSIONS,
                ALLOWED_FILE_TYPES,
                DEFAULT_REPLACEMENTS,
            )

            assert isinstance(ALLOWED_FILE_TYPES, (set, frozenset, list, tuple))
            assert isinstance(ALLOWED_EXTENSIONS, (set, frozenset, list, tuple))
            assert isinstance(DEFAULT_REPLACEMENTS, dict)
        except ImportError:
            pytest.skip("ha_rebrand.const not importable")
