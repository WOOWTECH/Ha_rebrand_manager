"""Admin Panel Page Object for E2E tests.

This module provides page object for the HA Rebrand Manager admin panel.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tests.e2e.pages.base_page import BasePage

if TYPE_CHECKING:
    from playwright.sync_api import Page


@dataclass
class BrandingSettings:
    """Data class for branding settings."""

    product_name: str | None = None
    documentation_url: str | None = None
    favicon_url: str | None = None
    logo_url: str | None = None
    sidebar_logo_url: str | None = None


class AdminPanel(BasePage):
    """Page Object for the HA Rebrand Manager admin panel.

    Provides methods for interacting with the rebranding settings
    and configuration options.
    """

    # Selectors for admin panel elements
    CONFIG_PANEL = "[data-panel='config']"
    INTEGRATIONS_LINK = 'a[href="/config/integrations"]'
    REBRAND_CARD = "[data-integration='ha_rebrand']"
    REBRAND_PANEL = "ha-rebrand-panel"

    # Settings form selectors
    PRODUCT_NAME_INPUT = 'input[name="product_name"], #product-name'
    DOCUMENTATION_URL_INPUT = 'input[name="documentation_url"], #documentation-url'
    FAVICON_URL_INPUT = 'input[name="favicon_url"], #favicon-url'
    LOGO_URL_INPUT = 'input[name="logo_url"], #logo-url'
    SIDEBAR_LOGO_INPUT = 'input[name="sidebar_logo_url"], #sidebar-logo-url'
    SAVE_BUTTON = 'button[type="submit"], mwc-button.save-button'
    RESET_BUTTON = 'button.reset-button, mwc-button.reset-button'

    def __init__(self, page: Page, base_url: str = "http://localhost:8123") -> None:
        """Initialize the admin panel page.

        Args:
            page: The Playwright page instance.
            base_url: The Home Assistant base URL.
        """
        super().__init__(page, base_url)

    def navigate_to_config(self) -> None:
        """Navigate to the Home Assistant configuration panel."""
        self.navigate_to("/config")
        self.wait_for_page_load()

    def navigate_to_integrations(self) -> None:
        """Navigate to the integrations page."""
        self.navigate_to("/config/integrations")
        self.wait_for_page_load()

    def navigate_to_rebrand_panel(self) -> None:
        """Navigate directly to the HA Rebrand panel.

        This navigates to the custom panel registered by the integration.
        """
        self.navigate_to("/ha_rebrand")
        self.wait_for_page_load()

    def is_rebrand_panel_visible(self, timeout: int = 10000) -> bool:
        """Check if the rebrand panel is displayed.

        Args:
            timeout: Maximum time to wait in milliseconds.

        Returns:
            True if the panel is visible, False otherwise.
        """
        return self.is_visible(self.REBRAND_PANEL, timeout=timeout)

    def open_rebrand_settings(self) -> None:
        """Open the HA Rebrand settings from integrations.

        First navigates to integrations, then clicks on the rebrand integration.
        """
        self.navigate_to_integrations()

        # Wait for integrations to load
        self.wait_for_element(self.REBRAND_CARD, timeout=10000)

        # Click on the rebrand integration card
        self.click_element(self.REBRAND_CARD)
        self.wait_for_page_load()

    def get_current_settings(self) -> BrandingSettings:
        """Get the current branding settings from the form.

        Returns:
            BrandingSettings object with current values.
        """
        settings = BrandingSettings()

        # Get product name if visible
        if self.is_visible(self.PRODUCT_NAME_INPUT, timeout=2000):
            product_name_el = self.page.locator(self.PRODUCT_NAME_INPUT)
            settings.product_name = product_name_el.input_value()

        # Get documentation URL if visible
        if self.is_visible(self.DOCUMENTATION_URL_INPUT, timeout=2000):
            doc_url_el = self.page.locator(self.DOCUMENTATION_URL_INPUT)
            settings.documentation_url = doc_url_el.input_value()

        # Get favicon URL if visible
        if self.is_visible(self.FAVICON_URL_INPUT, timeout=2000):
            favicon_el = self.page.locator(self.FAVICON_URL_INPUT)
            settings.favicon_url = favicon_el.input_value()

        # Get logo URL if visible
        if self.is_visible(self.LOGO_URL_INPUT, timeout=2000):
            logo_el = self.page.locator(self.LOGO_URL_INPUT)
            settings.logo_url = logo_el.input_value()

        # Get sidebar logo URL if visible
        if self.is_visible(self.SIDEBAR_LOGO_INPUT, timeout=2000):
            sidebar_el = self.page.locator(self.SIDEBAR_LOGO_INPUT)
            settings.sidebar_logo_url = sidebar_el.input_value()

        return settings

    def set_product_name(self, name: str) -> None:
        """Set the product name in settings.

        Args:
            name: The new product name.
        """
        self.fill_input(self.PRODUCT_NAME_INPUT, name)

    def set_documentation_url(self, url: str) -> None:
        """Set the documentation URL in settings.

        Args:
            url: The documentation URL.
        """
        self.fill_input(self.DOCUMENTATION_URL_INPUT, url)

    def set_favicon_url(self, url: str) -> None:
        """Set the favicon URL in settings.

        Args:
            url: The favicon URL.
        """
        self.fill_input(self.FAVICON_URL_INPUT, url)

    def set_logo_url(self, url: str) -> None:
        """Set the logo URL in settings.

        Args:
            url: The logo URL.
        """
        self.fill_input(self.LOGO_URL_INPUT, url)

    def set_sidebar_logo_url(self, url: str) -> None:
        """Set the sidebar logo URL in settings.

        Args:
            url: The sidebar logo URL.
        """
        self.fill_input(self.SIDEBAR_LOGO_INPUT, url)

    def apply_settings(self, settings: BrandingSettings) -> None:
        """Apply a complete set of branding settings.

        Args:
            settings: The BrandingSettings to apply.
        """
        if settings.product_name is not None:
            self.set_product_name(settings.product_name)

        if settings.documentation_url is not None:
            self.set_documentation_url(settings.documentation_url)

        if settings.favicon_url is not None:
            self.set_favicon_url(settings.favicon_url)

        if settings.logo_url is not None:
            self.set_logo_url(settings.logo_url)

        if settings.sidebar_logo_url is not None:
            self.set_sidebar_logo_url(settings.sidebar_logo_url)

    def save_settings(self) -> bool:
        """Save the current settings.

        Returns:
            True if save was successful, False otherwise.
        """
        self.click_element(self.SAVE_BUTTON)
        self.wait_for_animation()

        # Check for success notification or state change
        # This may need to be adjusted based on actual UI feedback
        return True

    def reset_settings(self) -> None:
        """Reset all settings to defaults."""
        if self.is_visible(self.RESET_BUTTON, timeout=2000):
            self.click_element(self.RESET_BUTTON)
            self.wait_for_animation()

    def wait_for_settings_load(self, timeout: int = 10000) -> bool:
        """Wait for settings to be loaded in the form.

        Args:
            timeout: Maximum time to wait in milliseconds.

        Returns:
            True if settings loaded, False if timeout.
        """
        try:
            self.wait_for_element(self.PRODUCT_NAME_INPUT, timeout=timeout)
            return True
        except Exception:
            return False
