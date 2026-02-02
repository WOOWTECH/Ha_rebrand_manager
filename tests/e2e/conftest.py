"""Pytest fixtures for E2E tests.

This module provides Playwright fixtures for browser automation
and Home Assistant authentication.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from typing import TYPE_CHECKING

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

if TYPE_CHECKING:
    from playwright.sync_api import Playwright

# Environment variables for Home Assistant connection
HA_URL = os.environ.get("HA_URL", "http://localhost:8123")
HA_USERNAME = os.environ.get("HA_USERNAME", "")
HA_PASSWORD = os.environ.get("HA_PASSWORD", "")


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Create a Playwright instance for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Create a Chromium browser instance.

    This fixture creates a single browser instance shared across
    all tests in the session for performance.
    """
    browser = playwright_instance.chromium.launch(
        headless=os.environ.get("HEADLESS", "true").lower() == "true",
        slow_mo=int(os.environ.get("SLOW_MO", "0")),
    )
    yield browser
    browser.close()


@pytest.fixture
def browser_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Create a fresh browser context for each test.

    Each test gets its own context with isolated cookies and storage.
    """
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    yield context
    context.close()


@pytest.fixture
def page(browser_context: BrowserContext) -> Generator[Page, None, None]:
    """Create a new page for each test."""
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture
def authenticated_page(page: Page) -> Page:
    """Create a page that is authenticated to Home Assistant.

    This fixture navigates to Home Assistant and performs login
    using credentials from environment variables.

    Raises:
        ValueError: If HA_USERNAME or HA_PASSWORD are not set.
    """
    if not HA_USERNAME or not HA_PASSWORD:
        pytest.skip("HA_USERNAME and HA_PASSWORD must be set for authenticated tests")

    # Navigate to Home Assistant
    page.goto(HA_URL)

    # Wait for login form or dashboard (already logged in)
    page.wait_for_load_state("networkidle")

    # Check if we need to login
    if page.locator('input[name="username"]').is_visible(timeout=5000):
        # Fill login form
        page.locator('input[name="username"]').fill(HA_USERNAME)
        page.locator('input[name="password"]').fill(HA_PASSWORD)

        # Click login button
        page.locator('button[type="submit"]').click()

        # Wait for dashboard to load
        page.wait_for_url(f"{HA_URL}/**", timeout=30000)
        page.wait_for_load_state("networkidle")

    return page


@pytest.fixture
def ha_url() -> str:
    """Return the Home Assistant URL."""
    return HA_URL


@pytest.fixture
def ha_credentials() -> dict[str, str]:
    """Return Home Assistant credentials."""
    return {
        "username": HA_USERNAME,
        "password": HA_PASSWORD,
    }
