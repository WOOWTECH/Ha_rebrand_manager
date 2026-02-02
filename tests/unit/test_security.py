"""Security unit tests for HA Rebrand component.

This module tests the security functions in ha_rebrand/__init__.py:
- _escape_js_string(): JavaScript string escaping for XSS prevention
- _validate_color(): CSS color validation to prevent injection
- File upload validation constants (ALLOWED_EXTENSIONS, ALLOWED_FILE_TYPES, MAX_FILE_SIZE)

Usage:
    pytest tests/unit/test_security.py -v
"""

from __future__ import annotations

import pytest

# Import security functions from ha_rebrand
from ha_rebrand import _escape_js_string, _validate_color

# Import constants for file upload validation
from ha_rebrand.const import ALLOWED_EXTENSIONS, ALLOWED_FILE_TYPES, MAX_FILE_SIZE

# Import test fixtures
from tests.fixtures.xss_payloads import (
    CSS_INJECTION_PAYLOADS,
    JS_ESCAPE_PAYLOADS,
    SAFE_STRINGS,
    XSS_PAYLOADS,
)
from tests.fixtures.sample_configs import SAMPLE_COLOR_VALUES


# =============================================================================
# _escape_js_string() Tests
# =============================================================================


class TestEscapeJsString:
    """Tests for the _escape_js_string() function."""

    def test_empty_string_returns_empty(self) -> None:
        """Test that empty string input returns empty string."""
        assert _escape_js_string("") == ""

    def test_none_returns_empty(self) -> None:
        """Test that None input returns empty string."""
        assert _escape_js_string(None) == ""

    @pytest.mark.parametrize(
        "payload",
        XSS_PAYLOADS,
        ids=lambda x: x[:40] if x else "empty",
    )
    def test_xss_payloads_escaped(self, payload: str) -> None:
        """Test that XSS payloads are properly escaped.

        The escaped output should not contain raw < or > characters
        that could be interpreted as HTML tags in a JavaScript context.
        """
        result = _escape_js_string(payload)

        # After escaping, raw angle brackets should be replaced with hex escapes
        assert "<" not in result, f"Unescaped '<' found in: {result}"
        assert ">" not in result, f"Unescaped '>' found in: {result}"

    @pytest.mark.parametrize(
        "payload",
        JS_ESCAPE_PAYLOADS,
        ids=lambda x: x[:40] if x else "empty",
    )
    def test_js_escape_payloads(self, payload: str) -> None:
        """Test that JavaScript-specific characters are escaped."""
        result = _escape_js_string(payload)

        # Should not contain unescaped quotes or special chars
        # Note: The function escapes these, so we check they're not raw
        if "'" in payload:
            assert "\\'" in result or "'" not in result
        if '"' in payload:
            assert '\\"' in result or '"' not in result

    def test_backslash_escaped(self) -> None:
        """Test that backslashes are properly escaped."""
        result = _escape_js_string("test\\path")
        assert "\\\\" in result

    def test_single_quote_escaped(self) -> None:
        """Test that single quotes are escaped."""
        result = _escape_js_string("it's a test")
        assert "\\'" in result

    def test_double_quote_escaped(self) -> None:
        """Test that double quotes are escaped."""
        result = _escape_js_string('say "hello"')
        assert '\\"' in result

    def test_newline_escaped(self) -> None:
        """Test that newlines are escaped."""
        result = _escape_js_string("line1\nline2")
        assert "\\n" in result
        assert "\n" not in result

    def test_carriage_return_escaped(self) -> None:
        """Test that carriage returns are escaped."""
        result = _escape_js_string("line1\rline2")
        assert "\\r" in result
        assert "\r" not in result

    def test_angle_brackets_escaped_to_hex(self) -> None:
        """Test that angle brackets are escaped to hex codes."""
        result = _escape_js_string("<script>alert(1)</script>")
        assert "\\x3c" in result  # <
        assert "\\x3e" in result  # >
        assert "<" not in result
        assert ">" not in result

    def test_script_tag_injection_prevented(self) -> None:
        """Test that script tag injection is prevented."""
        malicious = "</script><script>alert('xss')</script>"
        result = _escape_js_string(malicious)

        # The result should not be executable as HTML
        assert "<script>" not in result.lower()
        assert "</script>" not in result.lower()

    def test_normal_text_preserved(self) -> None:
        """Test that normal alphanumeric text is preserved."""
        result = _escape_js_string("Hello World 12345")
        assert result == "Hello World 12345"

    def test_unicode_preserved(self) -> None:
        """Test that unicode characters are preserved."""
        chinese = "\u4e2d\u6587"
        result = _escape_js_string(chinese)
        assert chinese in result

    @pytest.mark.parametrize(
        "safe_string",
        [s for s in SAFE_STRINGS if s and "<" not in s and ">" not in s],
        ids=lambda x: (x[:30] if x else "empty") if isinstance(x, str) else str(x)[:30],
    )
    def test_safe_strings_minimally_modified(self, safe_string: str) -> None:
        """Test that safe strings are not overly modified.

        Safe strings without special characters should pass through
        with minimal or no changes.
        """
        result = _escape_js_string(safe_string)
        # The result should still contain the core content
        # (quotes and backslashes will be escaped)
        assert len(result) >= len(safe_string.replace("'", "").replace('"', "").replace("\\", ""))


# =============================================================================
# _validate_color() Tests
# =============================================================================


class TestValidateColor:
    """Tests for the _validate_color() function."""

    def test_empty_string_returns_empty(self) -> None:
        """Test that empty string input returns empty string."""
        assert _validate_color("") == ""

    def test_none_returns_empty(self) -> None:
        """Test that None input returns empty string."""
        assert _validate_color(None) == ""

    @pytest.mark.parametrize(
        "color",
        SAMPLE_COLOR_VALUES["valid_hex_3"],
        ids=lambda x: x,
    )
    def test_valid_hex_3_colors(self, color: str) -> None:
        """Test that 3-character hex colors (#RGB) are accepted."""
        result = _validate_color(color)
        assert result == color

    @pytest.mark.parametrize(
        "color",
        SAMPLE_COLOR_VALUES["valid_hex_6"],
        ids=lambda x: x,
    )
    def test_valid_hex_6_colors(self, color: str) -> None:
        """Test that 6-character hex colors (#RRGGBB) are accepted."""
        result = _validate_color(color)
        assert result == color

    @pytest.mark.parametrize(
        "color",
        SAMPLE_COLOR_VALUES["valid_hex_8"],
        ids=lambda x: x,
    )
    def test_valid_hex_8_colors(self, color: str) -> None:
        """Test that 8-character hex colors (#RRGGBBAA) are accepted."""
        result = _validate_color(color)
        assert result == color

    @pytest.mark.parametrize(
        "color",
        SAMPLE_COLOR_VALUES["invalid"],
        ids=lambda x: x[:20] if x else "empty",
    )
    def test_invalid_colors_rejected(self, color: str) -> None:
        """Test that invalid color formats return empty string."""
        result = _validate_color(color)
        assert result == "", f"Invalid color '{color}' was not rejected"

    @pytest.mark.parametrize(
        "payload",
        CSS_INJECTION_PAYLOADS,
        ids=lambda x: x[:30] if x else "empty",
    )
    def test_css_injection_payloads_rejected(self, payload: str) -> None:
        """Test that CSS injection attempts are rejected."""
        result = _validate_color(payload)
        assert result == "", f"CSS injection payload '{payload}' was not rejected"

    def test_named_color_rejected(self) -> None:
        """Test that named colors like 'red' are rejected."""
        assert _validate_color("red") == ""
        assert _validate_color("blue") == ""
        assert _validate_color("transparent") == ""

    def test_rgb_function_rejected(self) -> None:
        """Test that rgb() function is rejected."""
        assert _validate_color("rgb(255, 0, 0)") == ""
        assert _validate_color("rgb(0,0,0)") == ""

    def test_rgba_function_rejected(self) -> None:
        """Test that rgba() function is rejected."""
        assert _validate_color("rgba(255, 0, 0, 0.5)") == ""

    def test_hsl_function_rejected(self) -> None:
        """Test that hsl() function is rejected."""
        assert _validate_color("hsl(0, 100%, 50%)") == ""

    def test_javascript_injection_rejected(self) -> None:
        """Test that JavaScript injection attempts in color are rejected."""
        assert _validate_color("expression(alert('xss'))") == ""
        assert _validate_color("url(javascript:alert('xss'))") == ""

    def test_css_property_injection_rejected(self) -> None:
        """Test that CSS property injection attempts are rejected."""
        assert _validate_color("#000;background:url(x)") == ""
        assert _validate_color("#000;}</style><script>alert(1)</script>") == ""

    def test_invalid_hex_characters_rejected(self) -> None:
        """Test that hex colors with invalid characters are rejected."""
        assert _validate_color("#GGG") == ""
        assert _validate_color("#ZZZZZZ") == ""
        assert _validate_color("#XYZ123") == ""

    def test_wrong_length_rejected(self) -> None:
        """Test that hex colors with wrong length are rejected."""
        assert _validate_color("#12") == ""  # Too short
        assert _validate_color("#12345") == ""  # 5 chars (invalid)
        assert _validate_color("#1234567") == ""  # 7 chars (invalid)
        assert _validate_color("#123456789") == ""  # 9 chars (too long)

    def test_missing_hash_rejected(self) -> None:
        """Test that colors without # prefix are rejected."""
        assert _validate_color("FFFFFF") == ""
        assert _validate_color("000") == ""

    def test_double_hash_rejected(self) -> None:
        """Test that colors with double # are rejected."""
        assert _validate_color("##FFFFFF") == ""

    def test_whitespace_in_color_rejected(self) -> None:
        """Test that colors with whitespace are rejected."""
        assert _validate_color(" #FFFFFF") == ""
        assert _validate_color("#FFFFFF ") == ""
        assert _validate_color("# FFFFFF") == ""

    def test_case_insensitive_hex(self) -> None:
        """Test that hex colors work with both upper and lower case."""
        assert _validate_color("#ffffff") == "#ffffff"
        assert _validate_color("#FFFFFF") == "#FFFFFF"
        assert _validate_color("#AbCdEf") == "#AbCdEf"


# =============================================================================
# File Upload Validation Constants Tests
# =============================================================================


class TestFileUploadConstants:
    """Tests for file upload validation constants."""

    def test_allowed_extensions_is_set(self) -> None:
        """Test that ALLOWED_EXTENSIONS is a set."""
        assert isinstance(ALLOWED_EXTENSIONS, set)

    def test_allowed_extensions_not_empty(self) -> None:
        """Test that ALLOWED_EXTENSIONS contains values."""
        assert len(ALLOWED_EXTENSIONS) > 0

    @pytest.mark.parametrize(
        "extension",
        [".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp"],
    )
    def test_expected_extensions_allowed(self, extension: str) -> None:
        """Test that expected image extensions are in ALLOWED_EXTENSIONS."""
        assert extension in ALLOWED_EXTENSIONS, f"{extension} should be allowed"

    @pytest.mark.parametrize(
        "extension",
        [".js", ".html", ".php", ".exe", ".sh", ".py", ".bat", ".cmd"],
    )
    def test_dangerous_extensions_not_allowed(self, extension: str) -> None:
        """Test that dangerous/executable extensions are not allowed."""
        assert extension not in ALLOWED_EXTENSIONS, f"{extension} should not be allowed"

    def test_extensions_are_lowercase(self) -> None:
        """Test that all extensions are lowercase for consistent comparison."""
        for ext in ALLOWED_EXTENSIONS:
            assert ext == ext.lower(), f"Extension {ext} should be lowercase"

    def test_extensions_start_with_dot(self) -> None:
        """Test that all extensions start with a dot."""
        for ext in ALLOWED_EXTENSIONS:
            assert ext.startswith("."), f"Extension {ext} should start with '.'"

    def test_allowed_file_types_is_set(self) -> None:
        """Test that ALLOWED_FILE_TYPES is a set."""
        assert isinstance(ALLOWED_FILE_TYPES, set)

    def test_allowed_file_types_not_empty(self) -> None:
        """Test that ALLOWED_FILE_TYPES contains values."""
        assert len(ALLOWED_FILE_TYPES) > 0

    @pytest.mark.parametrize(
        "file_type",
        ["logo", "logo_dark", "favicon"],
    )
    def test_expected_file_types_allowed(self, file_type: str) -> None:
        """Test that expected file types are in ALLOWED_FILE_TYPES."""
        assert file_type in ALLOWED_FILE_TYPES, f"{file_type} should be allowed"

    def test_arbitrary_file_types_not_allowed(self) -> None:
        """Test that arbitrary file types are not allowed."""
        assert "script" not in ALLOWED_FILE_TYPES
        assert "config" not in ALLOWED_FILE_TYPES
        assert "system" not in ALLOWED_FILE_TYPES

    def test_max_file_size_is_positive_int(self) -> None:
        """Test that MAX_FILE_SIZE is a positive integer."""
        assert isinstance(MAX_FILE_SIZE, int)
        assert MAX_FILE_SIZE > 0

    def test_max_file_size_reasonable(self) -> None:
        """Test that MAX_FILE_SIZE is a reasonable value (between 1MB and 50MB)."""
        one_mb = 1024 * 1024
        fifty_mb = 50 * 1024 * 1024
        assert one_mb <= MAX_FILE_SIZE <= fifty_mb, \
            f"MAX_FILE_SIZE ({MAX_FILE_SIZE}) should be between 1MB and 50MB"

    def test_max_file_size_is_5mb(self) -> None:
        """Test that MAX_FILE_SIZE is exactly 5MB as expected."""
        expected = 5 * 1024 * 1024  # 5MB
        assert MAX_FILE_SIZE == expected, \
            f"MAX_FILE_SIZE should be 5MB ({expected}), got {MAX_FILE_SIZE}"


# =============================================================================
# Integration Tests - Combined Security Checks
# =============================================================================


class TestSecurityIntegration:
    """Integration tests combining multiple security functions."""

    def test_xss_payload_in_color_rejected(self) -> None:
        """Test that XSS payloads disguised as colors are rejected."""
        for payload in XSS_PAYLOADS[:10]:  # Test a subset
            result = _validate_color(payload)
            assert result == "", f"XSS payload as color was not rejected: {payload}"

    def test_escaped_string_safe_for_js_context(self) -> None:
        """Test that escaped strings are safe for JavaScript string context."""
        dangerous = "<script>alert(document.cookie)</script>"
        escaped = _escape_js_string(dangerous)

        # The escaped string should be safely embeddable in JS
        js_code = f'var x = "{escaped}";'

        # Should not contain unescaped script tags
        assert "<script>" not in js_code
        assert "</script>" not in js_code

    def test_color_and_js_escape_combined(self) -> None:
        """Test color validation followed by JS escaping for compound attacks."""
        # Attacker might try to inject both CSS and JS
        attack = "#000;alert('xss')"

        # Color validation should reject this
        color_result = _validate_color(attack)
        assert color_result == ""

        # If someone bypassed color validation, JS escape should still help
        js_result = _escape_js_string(attack)
        assert "'" not in js_result or "\\'" in js_result
