from pages.base_page import BasePage
from playwright.sync_api import Page


class HomePage(BasePage):
    """Page Object for the Home page - handles navigation to services."""

    def __init__(self, page: Page):
        super().__init__(page)

    def accept_cookies(self):
        """Accept cookie consent if dialog appears."""
        try:
            cookie_accept_selectors = [
                'button:has-text("Accept")',
                'button:has-text("Accept All")',
                'button:has-text("Allow")',
                'button:has-text("Accept all")',
                '[data-cookie="accept"]',
                '#cookie-accept',
                '.cookie-accept',
            ]
            for selector in cookie_accept_selectors:
                try:
                    btn = self.page.locator(selector).first
                    if btn.is_visible(timeout=2000):
                        btn.click()
                        self.page.wait_for_timeout(500)
                        return True
                except Exception:
                    continue
        except Exception:
            pass
        return False

    def close_modal_if_exists(self):
        """Close any open modal popups."""
        try:
            # Look for modal close buttons
            close_selectors = [
                'button[aria-label="Close"]',
                'button:has-text("Close")',
                '.modal-close',
                '[data-testid="close-modal"]',
                'button[class*="close"]',
                '.app-modal-close',
            ]
            for selector in close_selectors:
                close_btn = self.page.locator(selector).first
                if close_btn.is_visible(timeout=2000):
                    close_btn.click()
                    self.page.wait_for_timeout(500)
                    return True
        except Exception:
            pass

        # Also try pressing Escape key
        try:
            self.page.keyboard.press('Escape')
            self.page.wait_for_timeout(500)
        except Exception:
            pass

        return False

    def click_our_services(self):
        """Click on Our Services button/link in navigation."""
        # Close any modal first
        self.close_modal_if_exists()

        # Click the anchor tag (first one), not the heading
        locator = self.page.locator('a:has-text("Our Services")').first
        locator.wait_for(state="visible", timeout=30000)
        locator.click()

    def click_home_energy_assessment(self):
        """Click on Home Energy Assessment card/link."""
        # Close any modal first
        self.close_modal_if_exists()

        # Find all links with "Home Energy Assessment" and click the visible one
        all_links = self.page.locator('a:has-text("Home Energy Assessment")').all()
        for link in all_links:
            try:
                if link.is_visible():
                    link.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(300)
                    link.click()
                    return
            except Exception:
                continue

        # If no visible link found, try clicking the last one (usually visible in content)
        if all_links:
            all_links[-1].click()

    def click_book_assessment(self):
        """Click on Book assessment button."""
        # Close any modal first
        self.close_modal_if_exists()

        # Try various "Book" buttons
        try:
            # Look for "Book Your Assessment" or "Book your Home Energy Assessment"
            locator = self.page.locator('a:has-text("Book"), button:has-text("Book")').all()
            for btn in locator:
                if btn.is_visible():
                    text = btn.inner_text().lower()
                    if "book" in text and ("assessment" in text or "your" in text):
                        btn.click()
                        return
        except Exception:
            pass

        # Fallback: first Book button
        try:
            locator = self.page.get_by_text("Book").first
            locator.wait_for(state="visible", timeout=30000)
            locator.click()
        except Exception:
            # Last resort: any button with "Book"
            self.page.click('a:has-text("Book"):first')

    def navigate_to_booking(self):
        """Complete navigation flow from home to booking page."""
        self.accept_cookies()
        self.page.wait_for_timeout(500)
        self.click_our_services()
        self.page.wait_for_timeout(2000)  # Wait for page load
        self.accept_cookies()
        self.page.wait_for_timeout(500)
        self.click_home_energy_assessment()
        self.page.wait_for_timeout(2000)  # Wait for page load
        self.accept_cookies()
        self.page.wait_for_timeout(500)
        self.click_book_assessment()
        self.accept_cookies()
        self.page.wait_for_timeout(1000)
