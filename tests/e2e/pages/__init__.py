"""Page Object Model classes for E2E tests.

This package provides page abstractions for interacting with
Home Assistant's web interface during E2E testing.
"""

from tests.e2e.pages.admin_panel import AdminPanel
from tests.e2e.pages.base_page import BasePage
from tests.e2e.pages.login_page import LoginPage
from tests.e2e.pages.sidebar import Sidebar

__all__ = ["BasePage", "LoginPage", "AdminPanel", "Sidebar"]
