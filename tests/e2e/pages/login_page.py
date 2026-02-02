"""Login Page Object for E2E tests.

This module provides page object for Home Assistant login interactions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.e2e.pages.base_page import BasePage

if TYPE_CHECKING:
    from playwright.sync_api import Page


class LoginPage(BasePage):
    """Page Object for the Home Assistant login page.

    Provides methods for interacting with the login form
    and handling authentication.
    """

    # Selectors for login page elements
    USERNAME_INPUT = 'input[name="username"]'
    PASSWORD_INPUT = 'input[name="password"]'
    SUBMIT_BUTTON = 'button[type="submit"]'
    ERROR_MESSAGE = ".error-message"
    ONBOARDING_SELECTOR = "ha-onboarding"

    def __init__(self, page: Page, base_url: str = "http://localhost:8123") -> None:
        """Initialize the login page.

        Args:
            page: The Playwright page instance.
            base_url: The Home Assistant base URL.
        """
        super().__init__(page, base_url)

    def navigate_to_login(self) -> None:
        """Navigate to the Home Assistant login page."""
        self.navigate_to("/")

    def is_login_page_visible(self, timeout: int = 10000) -> bool:
        """Check if the login page is displayed.

        Args:
            timeout: Maximum time to wait in milliseconds.

        Returns:
            True if login form is visible, False otherwise.
        """
        return self.is_visible(self.USERNAME_INPUT, timeout=timeout)

    def is_onboarding_page(self, timeout: int = 5000) -> bool:
        """Check if this is the onboarding page (fresh HA install).

        Args:
            timeout: Maximum time to wait in milliseconds.

        Returns:
            True if onboarding page is shown, False otherwise.
        """
        return self.is_visible(self.ONBOARDING_SELECTOR, timeout=timeout)

    def enter_username(self, username: str) -> None:
        """Enter the username in the login form.

        Args:
            username: The username to enter.
        """
        self.fill_input(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Enter the password in the login form.

        Args:
            password: The password to enter.
        """
        self.fill_input(self.PASSWORD_INPUT, password)

    def click_submit(self) -> None:
        """Click the submit button to login."""
        self.click_element(self.SUBMIT_BUTTON)

    def login(self, username: str, password: str) -> bool:
        """Perform a complete login.

        Args:
            username: The username to login with.
            password: The password to login with.

        Returns:
            True if login was successful, False otherwise.
        """
        self.navigate_to_login()
        self.wait_for_page_load()

        # Check if already logged in (redirected to dashboard)
        if not self.is_login_page_visible(timeout=5000):
            return True

        # Enter credentials
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()

        # Wait for navigation
        self.wait_for_page_load()

        # Check if login was successful (no longer on login page)
        return not self.is_login_page_visible(timeout=3000)

    def get_error_message(self) -> str | None:
        """Get the login error message if present.

        Returns:
            The error message text, or None if no error is displayed.
        """
        if self.is_visible(self.ERROR_MESSAGE, timeout=2000):
            return self.get_text(self.ERROR_MESSAGE)
        return None

    def logout(self) -> None:
        """Logout from Home Assistant.

        Navigates to profile and clicks logout.
        """
        # Open profile menu
        self.navigate_to("/profile")
        self.wait_for_page_load()

        # Click logout button
        logout_button = self.page.get_by_text("Log out")
        if logout_button.is_visible():
            logout_button.click()
            self.wait_for_page_load()

    def wait_for_dashboard(self, timeout: int = 30000) -> bool:
        """Wait for the dashboard to load after login.

        Args:
            timeout: Maximum time to wait in milliseconds.

        Returns:
            True if dashboard loaded, False if timeout.
        """
        try:
            # Wait for the main content to load
            self.page.wait_for_selector(
                "home-assistant, ha-panel-lovelace, hui-root",
                timeout=timeout,
            )
            return True
        except Exception:
            return False
