"""Sidebar Page Object for E2E tests.

This module provides page object for verifying sidebar branding changes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.e2e.pages.base_page import BasePage

if TYPE_CHECKING:
    from playwright.sync_api import Page


class Sidebar(BasePage):
    """Page Object for the Home Assistant sidebar.

    Provides methods for verifying branding changes in the sidebar,
    including logo, product name, and navigation elements.
    """

    # Selectors for sidebar elements
    SIDEBAR = "ha-sidebar, .sidebar"
    SIDEBAR_LOGO = ".sidebar-logo, ha-sidebar-logo, .logo img"
    SIDEBAR_TITLE = ".menu .title, .sidebar-title"
    SIDEBAR_TOGGLE = ".menu-toggle, ha-icon-button.menu-toggle"
    MENU_ITEMS = ".menu a, paper-item"

    # Branding-specific selectors
    CUSTOM_LOGO = ".sidebar-logo img, ha-sidebar-logo img"
    PRODUCT_NAME_ELEMENT = ".product-name, .sidebar-title .name"

    def __init__(self, page: Page, base_url: str = "http://localhost:8123") -> None:
        """Initialize the sidebar page object.

        Args:
            page: The Playwright page instance.
            base_url: The Home Assistant base URL.
        """
        super().__init__(page, base_url)

    def is_sidebar_visible(self, timeout: int = 10000) -> bool:
        """Check if the sidebar is visible.

        Args:
            timeout: Maximum time to wait in milliseconds.

        Returns:
            True if sidebar is visible, False otherwise.
        """
        return self.is_visible(self.SIDEBAR, timeout=timeout)

    def toggle_sidebar(self) -> None:
        """Toggle the sidebar open/closed state."""
        if self.is_visible(self.SIDEBAR_TOGGLE, timeout=2000):
            self.click_element(self.SIDEBAR_TOGGLE)
            self.wait_for_animation()

    def get_sidebar_logo_src(self) -> str | None:
        """Get the source URL of the sidebar logo.

        Returns:
            The logo src attribute, or None if not found.
        """
        if self.is_visible(self.CUSTOM_LOGO, timeout=5000):
            logo = self.page.locator(self.CUSTOM_LOGO).first
            return logo.get_attribute("src")
        return None

    def get_sidebar_title(self) -> str | None:
        """Get the sidebar title/product name.

        Returns:
            The title text, or None if not found.
        """
        if self.is_visible(self.SIDEBAR_TITLE, timeout=5000):
            return self.get_text(self.SIDEBAR_TITLE)
        return None

    def has_custom_logo(self) -> bool:
        """Check if a custom logo is displayed in the sidebar.

        Returns:
            True if a custom logo is visible, False otherwise.
        """
        return self.is_visible(self.CUSTOM_LOGO, timeout=5000)

    def verify_product_name(self, expected_name: str) -> bool:
        """Verify the product name matches the expected value.

        Args:
            expected_name: The expected product name.

        Returns:
            True if the product name matches, False otherwise.
        """
        title = self.get_sidebar_title()
        if title is None:
            return False
        return expected_name.lower() in title.lower()

    def verify_logo_url(self, expected_url: str) -> bool:
        """Verify the logo URL matches the expected value.

        Args:
            expected_url: The expected logo URL.

        Returns:
            True if the logo URL matches, False otherwise.
        """
        logo_src = self.get_sidebar_logo_src()
        if logo_src is None:
            return False
        return expected_url in logo_src

    def get_menu_items(self) -> list[str]:
        """Get all menu items in the sidebar.

        Returns:
            A list of menu item text values.
        """
        items = []
        menu_locator = self.page.locator(self.MENU_ITEMS)
        count = menu_locator.count()

        for i in range(count):
            item = menu_locator.nth(i)
            text = item.text_content()
            if text:
                items.append(text.strip())

        return items

    def navigate_to_menu_item(self, item_text: str) -> bool:
        """Navigate to a menu item by its text.

        Args:
            item_text: The text of the menu item to click.

        Returns:
            True if navigation was successful, False otherwise.
        """
        menu_locator = self.page.locator(self.MENU_ITEMS)
        count = menu_locator.count()

        for i in range(count):
            item = menu_locator.nth(i)
            text = item.text_content()
            if text and item_text.lower() in text.lower():
                item.click()
                self.wait_for_page_load()
                return True

        return False

    def verify_branding_applied(
        self,
        product_name: str | None = None,
        logo_url: str | None = None,
    ) -> dict[str, bool]:
        """Verify that branding settings have been applied.

        Args:
            product_name: Expected product name (optional).
            logo_url: Expected logo URL (optional).

        Returns:
            Dictionary with verification results for each setting.
        """
        results: dict[str, bool] = {}

        if product_name is not None:
            results["product_name"] = self.verify_product_name(product_name)

        if logo_url is not None:
            results["logo_url"] = self.verify_logo_url(logo_url)

        results["sidebar_visible"] = self.is_sidebar_visible()
        results["has_custom_logo"] = self.has_custom_logo()

        return results

    def wait_for_branding_update(self, timeout: int = 5000) -> None:
        """Wait for branding changes to take effect.

        Args:
            timeout: Maximum time to wait in milliseconds.
        """
        # Wait for any animations
        self.wait_for_animation(duration=500)

        # Wait for network requests to complete
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def check_favicon(self) -> str | None:
        """Get the current favicon URL.

        Returns:
            The favicon href, or None if not found.
        """
        favicon = self.page.locator('link[rel="icon"], link[rel="shortcut icon"]')
        if favicon.count() > 0:
            return favicon.first.get_attribute("href")
        return None

    def verify_favicon_url(self, expected_url: str) -> bool:
        """Verify the favicon URL matches the expected value.

        Args:
            expected_url: The expected favicon URL.

        Returns:
            True if the favicon URL matches, False otherwise.
        """
        favicon_href = self.check_favicon()
        if favicon_href is None:
            return False
        return expected_url in favicon_href

    def get_page_title(self) -> str:
        """Get the browser page title.

        Returns:
            The page title text.
        """
        return self.page.title()

    def verify_page_title(self, expected_title: str) -> bool:
        """Verify the page title contains the expected text.

        Args:
            expected_title: The expected title text.

        Returns:
            True if the title matches, False otherwise.
        """
        title = self.get_page_title()
        return expected_title.lower() in title.lower()
