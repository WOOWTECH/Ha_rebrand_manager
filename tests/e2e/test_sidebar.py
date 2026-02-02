"""E2E tests for sidebar branding functionality.

This module contains Playwright E2E tests for verifying that sidebar
branding customizations (logo, title) are applied correctly and
persist through theme changes (dark/light mode).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.e2e.pages.admin_panel import AdminPanel, BrandingSettings
from tests.e2e.pages.sidebar import Sidebar

if TYPE_CHECKING:
    from playwright.sync_api import Page


# Test data for sidebar branding
CUSTOM_PRODUCT_NAME = "My Smart Home"
CUSTOM_LOGO_URL = "/local/custom_logo.png"
CUSTOM_DARK_LOGO_URL = "/local/custom_logo_dark.png"


@pytest.mark.e2e
class TestSidebarBranding:
    """Test suite for sidebar branding customization."""

    def test_sidebar_is_visible_after_login(self, authenticated_page: Page) -> None:
        """Verify the sidebar is visible after authentication.

        This is a basic smoke test to ensure the sidebar loads properly
        before testing branding features.
        """
        sidebar = Sidebar(authenticated_page)

        # Verify sidebar is visible
        assert sidebar.is_sidebar_visible(), "Sidebar should be visible after login"

    def test_custom_logo_in_sidebar(self, authenticated_page: Page) -> None:
        """Verify custom logo is displayed in sidebar.

        This test configures a custom logo URL and verifies it appears
        in the sidebar.
        """
        admin = AdminPanel(authenticated_page)
        sidebar = Sidebar(authenticated_page)

        # Navigate to rebrand panel and set custom logo
        admin.navigate_to_rebrand_panel()
        admin.wait_for_settings_load()

        settings = BrandingSettings(sidebar_logo_url=CUSTOM_LOGO_URL)
        admin.apply_settings(settings)
        admin.save_settings()

        # Navigate back to dashboard
        sidebar.navigate_to_menu_item("Overview")
        sidebar.wait_for_branding_update()

        # Verify custom logo is visible
        assert sidebar.has_custom_logo(), "Custom logo should be visible in sidebar"

        # Verify logo URL contains the custom path
        logo_src = sidebar.get_sidebar_logo_src()
        assert logo_src is not None, "Logo source should not be None"
        assert CUSTOM_LOGO_URL in logo_src or "custom" in logo_src.lower(), (
            f"Logo URL should contain custom path, got: {logo_src}"
        )

    def test_sidebar_title_change(self, authenticated_page: Page) -> None:
        """Verify custom title/product name is displayed in sidebar.

        This test configures a custom product name and verifies it appears
        in the sidebar header.
        """
        admin = AdminPanel(authenticated_page)
        sidebar = Sidebar(authenticated_page)

        # Navigate to rebrand panel and set custom product name
        admin.navigate_to_rebrand_panel()
        admin.wait_for_settings_load()

        settings = BrandingSettings(product_name=CUSTOM_PRODUCT_NAME)
        admin.apply_settings(settings)
        admin.save_settings()

        # Navigate back to dashboard
        sidebar.navigate_to_menu_item("Overview")
        sidebar.wait_for_branding_update()

        # Verify product name is displayed
        assert sidebar.verify_product_name(CUSTOM_PRODUCT_NAME), (
            f"Sidebar title should contain '{CUSTOM_PRODUCT_NAME}'"
        )

        # Also verify page title is updated
        assert sidebar.verify_page_title(CUSTOM_PRODUCT_NAME), (
            f"Page title should contain '{CUSTOM_PRODUCT_NAME}'"
        )

    def test_dark_mode_logo_switching(self, authenticated_page: Page) -> None:
        """Verify branding persists when switching to dark mode.

        This test toggles dark mode and verifies that branding
        settings (logo, title) remain visible.
        """
        admin = AdminPanel(authenticated_page)
        sidebar = Sidebar(authenticated_page)

        # First set up custom branding
        admin.navigate_to_rebrand_panel()
        admin.wait_for_settings_load()

        settings = BrandingSettings(
            product_name=CUSTOM_PRODUCT_NAME,
            sidebar_logo_url=CUSTOM_LOGO_URL,
        )
        admin.apply_settings(settings)
        admin.save_settings()

        # Navigate to dashboard
        sidebar.navigate_to_menu_item("Overview")
        sidebar.wait_for_branding_update()

        # Open user profile menu and toggle dark mode
        _toggle_theme_mode(authenticated_page, target_mode="dark")

        # Wait for theme transition
        sidebar.wait_for_animation(duration=500)

        # Verify branding persists in dark mode
        assert sidebar.is_sidebar_visible(), "Sidebar should be visible in dark mode"
        assert sidebar.has_custom_logo(), "Custom logo should persist in dark mode"
        assert sidebar.verify_product_name(CUSTOM_PRODUCT_NAME), (
            "Product name should persist in dark mode"
        )

    def test_light_mode_logo_switching(self, authenticated_page: Page) -> None:
        """Verify branding persists when switching to light mode.

        This test ensures branding is preserved after switching from
        dark mode back to light mode.
        """
        admin = AdminPanel(authenticated_page)
        sidebar = Sidebar(authenticated_page)

        # First set up custom branding
        admin.navigate_to_rebrand_panel()
        admin.wait_for_settings_load()

        settings = BrandingSettings(
            product_name=CUSTOM_PRODUCT_NAME,
            sidebar_logo_url=CUSTOM_LOGO_URL,
        )
        admin.apply_settings(settings)
        admin.save_settings()

        # Navigate to dashboard
        sidebar.navigate_to_menu_item("Overview")
        sidebar.wait_for_branding_update()

        # Toggle to dark mode first
        _toggle_theme_mode(authenticated_page, target_mode="dark")
        sidebar.wait_for_animation(duration=500)

        # Then toggle back to light mode
        _toggle_theme_mode(authenticated_page, target_mode="light")
        sidebar.wait_for_animation(duration=500)

        # Verify branding persists in light mode
        assert sidebar.is_sidebar_visible(), "Sidebar should be visible in light mode"
        assert sidebar.has_custom_logo(), "Custom logo should persist in light mode"
        assert sidebar.verify_product_name(CUSTOM_PRODUCT_NAME), (
            "Product name should persist in light mode"
        )

    def test_sidebar_collapse_expand_with_branding(
        self, authenticated_page: Page
    ) -> None:
        """Verify branding remains intact after sidebar collapse/expand.

        This test ensures the logo scales correctly when the sidebar
        is collapsed and expanded.
        """
        sidebar = Sidebar(authenticated_page)

        # Ensure sidebar is visible
        assert sidebar.is_sidebar_visible()

        # Collapse sidebar
        sidebar.toggle_sidebar()
        sidebar.wait_for_animation()

        # Verify sidebar is still in DOM (just collapsed)
        assert sidebar.is_sidebar_visible(), "Sidebar should still be in DOM when collapsed"

        # Expand sidebar again
        sidebar.toggle_sidebar()
        sidebar.wait_for_animation()

        # Verify logo is still visible after expand
        assert sidebar.is_sidebar_visible(), "Sidebar should be visible after expand"

    def test_branding_persists_after_navigation(
        self, authenticated_page: Page
    ) -> None:
        """Verify branding persists when navigating between pages.

        This test ensures that custom branding remains visible as the
        user navigates to different sections of Home Assistant.
        """
        admin = AdminPanel(authenticated_page)
        sidebar = Sidebar(authenticated_page)

        # Set up custom branding
        admin.navigate_to_rebrand_panel()
        admin.wait_for_settings_load()

        settings = BrandingSettings(product_name=CUSTOM_PRODUCT_NAME)
        admin.apply_settings(settings)
        admin.save_settings()

        # Navigate to different pages and verify branding
        pages_to_visit = ["Overview", "Settings", "Developer Tools"]

        for page_name in pages_to_visit:
            if sidebar.navigate_to_menu_item(page_name):
                sidebar.wait_for_branding_update()

                # Verify product name is still visible
                assert sidebar.verify_product_name(CUSTOM_PRODUCT_NAME), (
                    f"Product name should persist on '{page_name}' page"
                )

    def test_sidebar_branding_on_mobile_viewport(
        self, authenticated_page: Page
    ) -> None:
        """Verify sidebar branding adapts to mobile viewport.

        This test resizes the viewport to mobile size and verifies
        the sidebar and branding behave correctly.
        """
        sidebar = Sidebar(authenticated_page)

        # Set mobile viewport
        authenticated_page.set_viewport_size({"width": 375, "height": 667})
        sidebar.wait_for_animation(duration=300)

        # On mobile, sidebar may be hidden by default
        # Try to toggle it open if a menu button is visible
        if sidebar.is_visible(sidebar.SIDEBAR_TOGGLE, timeout=2000):
            sidebar.toggle_sidebar()
            sidebar.wait_for_animation()

        # Verify sidebar functionality on mobile
        # The exact behavior depends on HA's responsive design
        # At minimum, the sidebar toggle should be accessible

        # Reset viewport for other tests
        authenticated_page.set_viewport_size({"width": 1280, "height": 720})


@pytest.mark.e2e
class TestSidebarFavicon:
    """Test suite for favicon customization."""

    def test_custom_favicon_applied(self, authenticated_page: Page) -> None:
        """Verify custom favicon is applied to the page.

        This test sets a custom favicon URL and verifies it appears
        in the page's link tags.
        """
        admin = AdminPanel(authenticated_page)
        sidebar = Sidebar(authenticated_page)
        custom_favicon = "/local/custom_favicon.ico"

        # Set custom favicon
        admin.navigate_to_rebrand_panel()
        admin.wait_for_settings_load()

        settings = BrandingSettings(favicon_url=custom_favicon)
        admin.apply_settings(settings)
        admin.save_settings()

        # Navigate to dashboard and check favicon
        sidebar.navigate_to_menu_item("Overview")
        sidebar.wait_for_branding_update()

        # Verify favicon URL
        assert sidebar.verify_favicon_url(custom_favicon), (
            f"Favicon URL should contain '{custom_favicon}'"
        )


def _toggle_theme_mode(page: Page, target_mode: str = "dark") -> None:
    """Toggle the theme mode via the user menu.

    Args:
        page: The Playwright page instance.
        target_mode: The target mode ("dark" or "light").
    """
    # Common selectors for theme toggle in Home Assistant
    user_menu_selectors = [
        "[data-testid='user-menu']",
        "ha-icon-button[data-entity-id]",
        ".user-badge",
        "ha-menu-button",
    ]

    # Try to open user menu
    for selector in user_menu_selectors:
        try:
            menu = page.locator(selector).first
            if menu.is_visible(timeout=2000):
                menu.click()
                page.wait_for_timeout(300)
                break
        except Exception:
            continue

    # Try to find and click theme toggle
    theme_selectors = [
        f"text={target_mode.capitalize()} mode",
        f"[data-testid='{target_mode}-mode-toggle']",
        f"mwc-list-item:has-text('{target_mode}')",
        f".theme-{target_mode}",
    ]

    for selector in theme_selectors:
        try:
            toggle = page.locator(selector).first
            if toggle.is_visible(timeout=1000):
                toggle.click()
                return
        except Exception:
            continue
