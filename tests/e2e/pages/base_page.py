"""Base Page Object for E2E tests.

This module provides common functionality shared across all page objects.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Locator, Page


class BasePage:
    """Base class for all Page Objects.

    Provides common navigation, wait utilities, and helper methods
    that are shared across all page objects.
    """

    def __init__(self, page: Page, base_url: str = "http://localhost:8123") -> None:
        """Initialize the base page.

        Args:
            page: The Playwright page instance.
            base_url: The Home Assistant base URL.
        """
        self.page = page
        self.base_url = base_url.rstrip("/")

    def navigate_to(self, path: str = "") -> None:
        """Navigate to a path relative to the base URL.

        Args:
            path: The path to navigate to (e.g., "/config" or "/lovelace").
        """
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(url)
        self.wait_for_page_load()

    def wait_for_page_load(self, timeout: int = 30000) -> None:
        """Wait for the page to fully load.

        Args:
            timeout: Maximum time to wait in milliseconds.
        """
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def wait_for_element(
        self,
        selector: str,
        *,
        state: str = "visible",
        timeout: int = 10000,
    ) -> Locator:
        """Wait for an element to reach a specific state.

        Args:
            selector: The selector to locate the element.
            state: The state to wait for ("visible", "hidden", "attached", "detached").
            timeout: Maximum time to wait in milliseconds.

        Returns:
            The locator for the element.
        """
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        return locator

    def wait_for_text(
        self,
        text: str,
        *,
        selector: str | None = None,
        timeout: int = 10000,
    ) -> Locator:
        """Wait for specific text to appear on the page.

        Args:
            text: The text to wait for.
            selector: Optional selector to limit the search scope.
            timeout: Maximum time to wait in milliseconds.

        Returns:
            The locator containing the text.
        """
        if selector:
            locator = self.page.locator(selector).get_by_text(text)
        else:
            locator = self.page.get_by_text(text)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def click_element(
        self,
        selector: str,
        *,
        timeout: int = 10000,
        force: bool = False,
    ) -> None:
        """Click an element after waiting for it to be visible.

        Args:
            selector: The selector to locate the element.
            timeout: Maximum time to wait in milliseconds.
            force: Whether to force the click without waiting for actionability.
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.click(force=force)

    def fill_input(
        self,
        selector: str,
        value: str,
        *,
        timeout: int = 10000,
    ) -> None:
        """Fill an input field with a value.

        Args:
            selector: The selector to locate the input.
            value: The value to fill.
            timeout: Maximum time to wait in milliseconds.
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.fill(value)

    def get_text(self, selector: str, *, timeout: int = 10000) -> str:
        """Get the text content of an element.

        Args:
            selector: The selector to locate the element.
            timeout: Maximum time to wait in milliseconds.

        Returns:
            The text content of the element.
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        return locator.text_content() or ""

    def is_visible(self, selector: str, *, timeout: int = 5000) -> bool:
        """Check if an element is visible.

        Args:
            selector: The selector to locate the element.
            timeout: Maximum time to wait in milliseconds.

        Returns:
            True if the element is visible, False otherwise.
        """
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def take_screenshot(self, name: str) -> bytes:
        """Take a screenshot of the current page.

        Args:
            name: The name for the screenshot file.

        Returns:
            The screenshot as bytes.
        """
        return self.page.screenshot(path=f"screenshots/{name}.png", full_page=True)

    def get_current_url(self) -> str:
        """Get the current page URL.

        Returns:
            The current URL as a string.
        """
        return self.page.url

    def reload(self) -> None:
        """Reload the current page."""
        self.page.reload()
        self.wait_for_page_load()

    def go_back(self) -> None:
        """Navigate back in browser history."""
        self.page.go_back()
        self.wait_for_page_load()

    def press_key(self, key: str) -> None:
        """Press a keyboard key.

        Args:
            key: The key to press (e.g., "Enter", "Escape", "Tab").
        """
        self.page.keyboard.press(key)

    def wait_for_animation(self, duration: int = 300) -> None:
        """Wait for CSS animations to complete.

        Args:
            duration: Time to wait in milliseconds.
        """
        self.page.wait_for_timeout(duration)
