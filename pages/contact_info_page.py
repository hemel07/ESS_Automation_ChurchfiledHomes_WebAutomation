from pages.base_page import BasePage
from playwright.sync_api import Page


class ContactInfoPage(BasePage):
    """Page Object for Contact Information page."""

    # Locators
    FIRST_NAME_INPUT = 'input[name="firstName"], [placeholder*="First"], label:has-text("First name") + input, input[id*="first"]'
    LAST_NAME_INPUT = 'input[name="lastName"], [placeholder*="Last"], label:has-text("Last name") + input, input[id*="last"]'
    EMAIL_INPUT = 'input[name="email"], input[type="email"], [placeholder*="Email"], label:has-text("Email") + input'
    MOBILE_INPUT = 'input[name="mobile"], input[type="tel"], [placeholder*="Mobile"], label:has-text("Mobile") + input'
    ADDRESS_SEARCH_INPUT = 'input[name="address"], input[placeholder*="Address"], input[placeholder*="Property"], label:has-text("Property Address") + input, input[id*="address"]'
    ADDRESS_DROPDOWN_RESULT = '[role="listbox"] li, .address-result, [class*="address"] li, ul li'
    NEXT_BUTTON = 'button:has-text("Next"), [data-testid="next"], button[type="submit"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def fill_first_name(self, first_name: str):
        """Fill first name field."""
        self._fill_field(self.FIRST_NAME_INPUT, first_name)

    def fill_last_name(self, last_name: str):
        """Fill last name field."""
        self._fill_field(self.LAST_NAME_INPUT, last_name)

    def fill_email(self, email: str):
        """Fill email field."""
        self._fill_field(self.EMAIL_INPUT, email)

    def fill_mobile(self, mobile: str):
        """Fill mobile number field."""
        self._fill_field(self.MOBILE_INPUT, mobile)

    def _fill_field(self, selector: str, value: str):
        """Fill a field using multiple selector attempts."""
        selectors = selector.split(", ")
        for sel in selectors:
            try:
                element = self.page.locator(sel)
                if element.is_visible(timeout=2000):
                    element.fill(value)
                    return
            except Exception:
                continue

        # Fallback: find by label text
        if "First name" in selector:
            self.page.fill('label:has-text("First name") + input', value)
        elif "Last name" in selector:
            self.page.fill('label:has-text("Last name") + input', value)
        elif "Email" in selector:
            self.page.fill('label:has-text("Email") + input', value)
        elif "Mobile" in selector:
            self.page.fill('label:has-text("Mobile") + input', value)

    def search_address(self, search_term: str):
        """Search for property address."""
        selectors = self.ADDRESS_SEARCH_INPUT.split(", ")
        for sel in selectors:
            try:
                element = self.page.locator(sel)
                if element.is_visible(timeout=2000):
                    element.fill(search_term)
                    # Wait for dropdown results
                    self.page.wait_for_timeout(2000)
                    return
            except Exception:
                continue

    def select_address_from_dropdown(self, index: int = 0):
        """Select an address from the dropdown results."""
        try:
            # Wait for dropdown to appear
            self.page.wait_for_timeout(1000)

            # Try common dropdown selectors
            dropdown_selectors = [
                '[role="listbox"] li',
                '[class*="autocomplete"] li',
                '.address-result',
                'ul li',
                '[data-testid="address-option"]',
            ]

            for selector in dropdown_selectors:
                try:
                    options = self.page.locator(selector).all()
                    if len(options) > index:
                        options[index].click()
                        return
                except Exception:
                    continue
        except Exception:
            pass

    def click_next(self):
        """Click Next button."""
        self.click_text("Next")

    def fill_contact_info(
        self,
        first_name: str,
        last_name: str,
        email: str,
        mobile: str,
        address: str = "Dublin",
    ):
        """Fill all contact information."""
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_email(email)
        self.fill_mobile(mobile)
        self.search_address(address)
        self.select_address_from_dropdown()
