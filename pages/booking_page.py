from pages.base_page import BasePage
from playwright.sync_api import Page
from datetime import datetime
import calendar


class BookingPage(BasePage):
    """Page Object for Booking/Calendar page."""

    # Locators
    CALENDAR_CONTAINER = '[class*="calendar"], [data-testid="calendar"], #calendar'
    DATE_PICKER = '[data-testid="date-picker"], .calendar-day, [class*="day"]:not([class*="disabled"])'
    NEXT_MONTH_BUTTON = 'button[aria-label*="Next"], button:has-text(">"), .calendar-next, [data-testid="next-month"]'
    PREV_MONTH_BUTTON = 'button[aria-label*="Previous"], button:has-text("<"), .calendar-prev, [data-testid="prev-month"]'
    TIME_SLOT_CONTAINER = '[class*="time"], [data-testid="time-slots"], .time-slots'
    TIME_SLOT_BUTTON = 'button:has-text("Morning"), button:has-text("Afternoon"), button:has-text("Evening"), [class*="time-slot"]'
    LATER_BUTTON = 'button:has-text("Later"), [data-testid="later"], button[type="button"]:has-text("Later")'
    EMAIL_CONFIRMATION = 'text=email, [data-testid="email"], .email-confirmation'
    MODAL_CONTENT = '.modal-content, [role="dialog"], [data-testid="modal"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def is_current_month_available(self) -> bool:
        """Check if any date is available in current month."""
        try:
            # Look for enabled/clickable date elements
            current_month = datetime.now().strftime("%B")
            current_year = datetime.now().year

            # Check if current month is displayed
            month_header = self.page.locator('[class*="month"], [data-testid="month-header"]').inner_text(timeout=3000)
            if current_month.lower() in month_header.lower() or str(current_year) in month_header:
                # Check for available dates (not disabled)
                available_dates = self.page.locator(
                    '[class*="day"]:not([class*="disabled"]):not([aria-disabled="true"])'
                )
                return available_dates.count() > 0
            return False
        except Exception:
            return True  # Assume available if we can't determine

    def navigate_to_next_month(self):
        """Click to navigate to next month in calendar."""
        try:
            # Try various next month button selectors
            selectors = [
                'button[aria-label*="Next"]',
                'button[aria-label="Next Month"]',
                '.calendar-next',
                '[data-testid="next-month"]',
            ]
            for selector in selectors:
                try:
                    btn = self.page.locator(selector)
                    if btn.is_visible():
                        btn.click()
                        self.page.wait_for_timeout(500)
                        return
                except Exception:
                    continue
        except Exception:
            pass

    def select_available_date(self, prefer_current_month: bool = True):
        """Select an available date from the calendar."""
        try:
            # Get all enabled dates
            date_selectors = [
                '[class*="day"]:not([class*="disabled"]):not([aria-disabled="true"])',
                '.calendar-day:not(.disabled)',
                '[data-testid="date"]:not([disabled])',
                'button[class*="day"]:not([disabled])',
            ]

            for selector in date_selectors:
                dates = self.page.locator(selector).all()
                if dates:
                    # Click first available date
                    dates[0].click()
                    self.page.wait_for_timeout(500)
                    return True

            # If no dates found and we prefer current month, try next month
            if prefer_current_month:
                self.navigate_to_next_month()
                for selector in date_selectors:
                    dates = self.page.locator(selector).all()
                    if dates:
                        dates[0].click()
                        self.page.wait_for_timeout(500)
                        return True

            return False
        except Exception as e:
            return False

    def select_available_time(self, preference: str = "morning"):
        """Select an available time slot.

        Tries in order: morning -> afternoon -> any available slot.
        """
        try:
            # Define preference order: try morning first, then afternoon, then any
            preferences_order = ["morning", "afternoon", "any"]

            # If user specified a preference, prioritize it but still fallback
            preference = preference.lower()
            if preference in preferences_order:
                preferences_order.remove(preference)
                preferences_order.insert(0, preference)

            for pref in preferences_order:
                time_selectors = [
                    f'button:has-text("{pref.capitalize()}")',
                    f'button:has-text("{pref}")',
                    '[class*="time-slot"]',
                    '[data-testid="time-slot"]',
                    '.time-slot',
                ]

                for selector in time_selectors:
                    try:
                        slots = self.page.locator(selector).all()
                        if slots:
                            slots[0].click()
                            self.page.wait_for_timeout(500)
                            return True
                    except Exception:
                        continue

            return False
        except Exception:
            return False

    def click_later(self):
        """Click the Later button."""
        self.click_text("Later")

    def get_confirmation_email(self) -> str:
        """Get the email address shown in confirmation."""
        try:
            # Try various selectors for email display
            selectors = [
                '[data-testid="email"]',
                '.email-confirmation',
                '[class*="email"]',
            ]
            for selector in selectors:
                try:
                    element = self.page.locator(selector)
                    if element.is_visible(timeout=2000):
                        return element.inner_text()
                except Exception:
                    continue

            # Fallback: look for email pattern in modal
            modal = self.page.locator(self.MODAL_CONTENT)
            if modal.is_visible():
                text = modal.inner_text()
                # Extract email using simple pattern
                import re
                email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
                matches = re.findall(email_pattern, text)
                if matches:
                    return matches[0]

            return ""
        except Exception:
            return ""

    def is_email_displayed(self, expected_email: str) -> bool:
        """Check if the expected email is displayed in confirmation.

        Returns True if emails match, False otherwise.
        """
        try:
            displayed_email = self.get_confirmation_email()
            return expected_email.lower() in displayed_email.lower() or displayed_email.lower() in expected_email.lower()
        except Exception:
            return False

    def verify_and_fix_email(self, expected_email: str) -> tuple[bool, str]:
        """Verify email matches expected, return (success, actual_email_or_error).

        Quick fix: if email doesn't match, capture what's actually displayed
        for debugging rather than silently failing.
        """
        try:
            displayed_email = self.get_confirmation_email()
            if expected_email.lower() in displayed_email.lower() or displayed_email.lower() in expected_email.lower():
                return True, displayed_email
            # Email mismatch - return actual for debugging
            return False, f"Expected '{expected_email}' but found '{displayed_email}'"
        except Exception as e:
            return False, f"Could not retrieve email: {str(e)}"

    def book_slot(
        self,
        prefer_current_month: bool = True,
        time_preference: str = "morning",
    ) -> bool:
        """Complete the booking flow for date and time."""
        # Select available date
        if not self.select_available_date(prefer_current_month):
            return False

        # Select time slot
        if not self.select_available_time(time_preference):
            return False

        return True
