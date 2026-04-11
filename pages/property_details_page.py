from pages.base_page import BasePage
from playwright.sync_api import Page
import os


class PropertyDetailsPage(BasePage):
    """Page Object for Property Details page."""

    def __init__(self, page: Page):
        super().__init__(page)

    def select_house_type(self, house_type: str):
        """Select house type using radio button."""
        # House types are radio buttons with labels
        # Map common names to label text
        house_type_map = {
            "Semi-detached": "Semi-Detached",
            "Semi-detatched": "Semi-Detached",
            "Detached": "Detached",
            "Mid-Terrace": "Mid-Terrace",
            "End of Terrace": "End of Terrace",
            "Basement Apartment": "Basement Apartment",
            "Ground-floor Apartment": "Ground-floor Apartment",
            "Ground-floor": "Ground-floor Apartment",
            "Mid-Floor Apartment": "Mid-Floor Apartment",
            "Top-Floor Apartment": "Top-Floor Apartment",
            "Maisonette": "Maisonette",
        }

        label_text = house_type_map.get(house_type, house_type)

        # Find the label and click it
        try:
            label = self.page.get_by_text(label_text, exact=False).first
            # Make sure it's in the house type section
            label.scroll_into_view_if_needed()
            self.page.wait_for_timeout(300)
            label.click()
            return
        except Exception:
            pass

        # Fallback: find radio button by value
        radio_selectors = [
            f'label:has-text("{label_text}")',
            f'input[value="{label_text.lower()}"]',
            f'input[id*="{house_type.lower().replace(" ", "-")}"]',
        ]

        for selector in radio_selectors:
            try:
                el = self.page.locator(selector)
                if el.is_visible():
                    if el.evaluate("el => el.tagName") == "INPUT":
                        el.check()
                    else:
                        el.click()
                    return
            except Exception:
                continue

    def select_storeys(self, storeys: str):
        """Select number of storeys using radio button."""
        # Map values to label text
        storey_map = {
            "1": "1 Storey",
            "2": "2 Storeys",
            "3": "3 Storeys",
        }

        label_text = storey_map.get(storeys, f"{storeys} Storey" if storeys == "1" else f"{storeys} Storeys")

        try:
            # Find label near "No. of storeys" section
            label = self.page.get_by_text(label_text, exact=False).first
            label.scroll_into_view_if_needed()
            self.page.wait_for_timeout(300)
            label.click()
            return
        except Exception:
            pass

        # Fallback: look for radio with specific value
        radio_selectors = [
            f'label:has-text("{label_text}")',
            f'input[value="{storeys}"]',
        ]

        for selector in radio_selectors:
            try:
                el = self.page.locator(selector)
                if el.is_visible():
                    if el.evaluate("el => el.tagName") == "INPUT":
                        el.check()
                    else:
                        el.click()
                    return
            except Exception:
                continue

    def select_extension_exists(self, value: bool = True):
        """Select whether extension exists (Yes/No radio)."""
        label_text = "Yes" if value else "No"

        # Find the Yes/No in the extension section
        try:
            # Look for label with text near "Is there any existing extension?"
            section = self.page.locator('text=Is there any existing extension?').first
            section.scroll_into_view_if_needed()

            # Find the Yes/No radio after this section
            label = self.page.locator(f'label:has-text("{label_text}")').all()
            for lbl in label:
                if lbl.is_visible():
                    # Check if it's near the extension question
                    parent_text = lbl.locator("..").inner_text()
                    if "extension" in parent_text.lower() or lbl.evaluate("el => el.querySelector('input[type=\"radio\"]')"):
                        lbl.click()
                        return
        except Exception:
            pass

        # Fallback: find radio by value
        value_str = "yes" if value else "no"
        try:
            radio = self.page.locator(f'input[type="radio"][value="{value_str}"]').first
            radio.check()
        except Exception:
            # Last resort: click any Yes/No label
            self.page.get_by_text(label_text, exact=True).first.click()

    def select_plans_extension(self, value: bool = True):
        """Select whether there are plans to add extension (Yes/No radio)."""
        label_text = "Yes" if value else "No"

        # Find the Yes/No in the plans extension section
        try:
            # Look for section about plans/adding extension
            section_text = "Plans to add extension"
            try:
                section = self.page.locator(f'text={section_text}').first
                section.scroll_into_view_if_needed()
            except Exception:
                pass

            # Find the Yes/No radio
            label = self.page.locator(f'label:has-text("{label_text}")').all()
            for lbl in label:
                if lbl.is_visible():
                    parent_text = lbl.locator("..").inner_text().lower()
                    if "plan" in parent_text and "extension" in parent_text:
                        lbl.click()
                        return
        except Exception:
            pass

        # Fallback: find second Yes/No group (after extension_exists)
        value_str = "yes" if value else "no"
        try:
            radios = self.page.locator(f'input[type="radio"][value="{value_str}"]').all()
            if len(radios) >= 2:
                radios[1].check()  # Second radio group is for plans
            else:
                radios[0].check()
        except Exception:
            pass

    def uncheck_photo_checkbox(self):
        """Uncheck 'I don't have a photo' checkbox."""
        try:
            # Find checkbox with this label
            label = self.page.get_by_text("I don't have a photo to hand").first
            if label.is_visible():
                checkbox = label.locator('input[type="checkbox"]')
                if checkbox.is_visible() and checkbox.is_checked():
                    checkbox.uncheck()
                elif checkbox.is_visible():
                    # Already unchecked
                    return
                else:
                    # Click the label to toggle
                    label.click()
                return
        except Exception:
            pass

        # Fallback: any checkbox near "photo" text
        try:
            checkboxes = self.page.locator('input[type="checkbox"]').all()
            for checkbox in checkboxes:
                if checkbox.is_visible():
                    parent = checkbox.locator("..")
                    text = parent.inner_text().lower()
                    if "photo" in text:
                        if checkbox.is_checked():
                            checkbox.uncheck()
                        return
        except Exception:
            pass

    def upload_photo(self, file_path: str):
        """Upload a photo file."""
        # Create test image if it doesn't exist
        if not os.path.exists(file_path):
            self._create_test_image(file_path)

        # Find file input
        try:
            file_input = self.page.locator('input[type="file"]').first
            file_input.wait_for(state="visible", timeout=5000)
            file_input.set_input_files(file_path)
            self.page.wait_for_timeout(500)  # Wait for upload
        except Exception:
            # Try clicking upload button first
            try:
                upload_btn = self.page.get_by_text("Upload").first
                upload_btn.click()
                self.page.wait_for_timeout(500)
                file_input = self.page.locator('input[type="file"]').first
                file_input.set_input_files(file_path)
            except Exception:
                pass  # May already have file input visible

    def _create_test_image(self, file_path: str):
        """Create a simple test image file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Create a minimal PNG file
        png_header = bytes([
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
            0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
            0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,
            0x54, 0x08, 0xD7, 0x63, 0xF8, 0xFF, 0xFF, 0x3F,
            0x00, 0x05, 0xFE, 0x02, 0xFE, 0xDC, 0xCC, 0x59,
            0xE7, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E,
            0x44, 0xAE, 0x42, 0x60, 0x82,
        ])
        with open(file_path, "wb") as f:
            f.write(png_header)

    def click_next(self):
        """Click Next button."""
        try:
            next_btn = self.page.get_by_text("Next", exact=True).first
            next_btn.scroll_into_view_if_needed()
            self.page.wait_for_timeout(300)
            next_btn.click()
        except Exception:
            # Try any button with "Next"
            self.page.click('button:has-text("Next")')

    def is_confirmation_visible(self) -> bool:
        """Check if confirmation text is visible."""
        return self.is_text_visible("Your first step to a warm, comfortable, and healthy home")

    def fill_property_details(
        self,
        house_type: str = "Semi-detached",
        storeys: str = "2",
        extension_exists: bool = True,
        plans_extension: bool = False,
        photo_path: str = None,
    ):
        """Fill all property details form."""
        self.select_house_type(house_type)
        self.page.wait_for_timeout(200)
        self.select_storeys(storeys)
        self.page.wait_for_timeout(200)
        self.select_extension_exists(extension_exists)
        self.page.wait_for_timeout(200)
        self.select_plans_extension(plans_extension)
        self.page.wait_for_timeout(200)
        self.uncheck_photo_checkbox()
        self.page.wait_for_timeout(200)

        if photo_path:
            self.upload_photo(photo_path)
            self.page.wait_for_timeout(500)

        self.click_next()
