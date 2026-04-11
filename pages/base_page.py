from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from typing import Optional
import time


class BasePage:
    """Base Page Object class with common methods for all pages."""

    def __init__(self, page: Page):
        self.page = page

    def click(self, locator: str, timeout: int = 30000):
        """Click an element using CSS selector."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        element.click()

    def click_text(self, text: str, exact: bool = False, timeout: int = 30000):
        """Click an element by text content."""
        if exact:
            locator = self.page.get_by_text(text, exact=True)
        else:
            locator = self.page.get_by_text(text, exact=False)
        locator.wait_for(state="visible", timeout=timeout)
        locator.click()

    def fill(self, locator: str, value: str, timeout: int = 30000):
        """Fill input field with value."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        element.fill(value)

    def select_dropdown(self, locator: str, value: str, timeout: int = 30000):
        """Select value from dropdown."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        element.select_option(value)

    def select_dropdown_by_label(self, label: str, value: str, timeout: int = 30000):
        """Select value from dropdown by label text."""
        self.page.select_option(f"label:has-text('{label}')", value, timeout=timeout)

    def is_visible(self, locator: str, timeout: int = 5000) -> bool:
        """Check if element is visible."""
        try:
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_text_visible(self, text: str, timeout: int = 5000) -> bool:
        """Check if text is visible on page."""
        try:
            locator = self.page.get_by_text(text)
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def wait_for_element(self, locator: str, timeout: int = 30000):
        """Wait for element to be visible."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        return element

    def wait_for_text(self, text: str, timeout: int = 30000):
        """Wait for text to be visible."""
        locator = self.page.get_by_text(text)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def close_popup_if_exists(self, timeout: int = 2000):
        """Close popup if it exists."""
        try:
            # Common popup close selectors
            popup_selectors = [
                'button[aria-label="Close"]',
                'button.close-modal',
                '.modal-close',
                '[data-testid="close-button"]',
                'button:has-text("Close")',
                'button:has-text("×")',
                'button:has-text("X")',
            ]
            for selector in popup_selectors:
                popup = self.page.locator(selector)
                if popup.is_visible(timeout=timeout):
                    popup.click()
                    time.sleep(0.5)
                    break
        except Exception:
            pass  # No popup to close

    def upload_file(self, locator: str, file_path: str, timeout: int = 30000):
        """Upload a file."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        element.set_input_files(file_path)

    def uncheck_checkbox(self, locator: str, timeout: int = 30000):
        """Uncheck a checkbox if it's checked."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        if element.is_checked():
            element.uncheck()

    def get_element_text(self, locator: str, timeout: int = 30000) -> str:
        """Get text content of an element."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        return element.inner_text()

    def hover(self, locator: str, timeout: int = 30000):
        """Hover over an element."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        element.hover()

    def scroll_into_view(self, locator: str, timeout: int = 30000):
        """Scroll element into view."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        element.scroll_into_view_if_needed()
