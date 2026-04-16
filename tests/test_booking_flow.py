"""
Test suite for ESS Home Energy Assessment booking flow.

This test automates the complete booking journey:
1. Navigate through services to Home Energy Assessment
2. Fill property details form
3. Fill contact information
4. Select booking date and time
5. Verify confirmation
"""

import pytest
import os
from datetime import datetime
from pages.home_page import HomePage
from pages.property_details_page import PropertyDetailsPage
from pages.contact_info_page import ContactInfoPage
from pages.booking_page import BookingPage


# Test data
TEST_DATA = {
    "house_type": "Semi-detached",
    "storeys": "2",
    "extension_exists": True,
    "plans_extension": False,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe.test@example.com",
    "mobile": "0871234567",
    "address_search": "Dublin",
    "time_preference": "morning",
}


@pytest.fixture
def test_image_path():
    """Provide path for test image upload.

    The image file is created on demand by PropertyDetailsPage._create_test_image()
    if it does not already exist, so we only need to ensure the directory is present.
    We intentionally do NOT delete the file after each test because multiple tests
    in the session reuse the same path.
    """
    test_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(test_dir, "..", "test_data", "test_image.png")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    yield image_path
    # No cleanup — the file is reused across tests and created on demand.


@pytest.mark.usefixtures("page")
class TestHomeEnergyAssessmentBooking:
    """Test class for Home Energy Assessment booking flow."""

    @pytest.mark.parametrize(
        "house_type,storeys,extension_exists,plans_extension",
        [
            ("Semi-detached", "2", True, False),
            ("Detached", "2", False, False),
            ("Terraced", "1", True, True),
        ],
        ids=["semi_2storey_ext", "detached_2storey_noext", "terraced_1storey_planext"],
    )
    def test_property_details_form(
        self,
        page,
        home_page,
        property_details_page,
        house_type,
        storeys,
        extension_exists,
        plans_extension,
        test_image_path,
    ):
        """Test property details form with various inputs."""
        # Navigate to booking
        home_page.navigate_to_booking()

        # Fill property details
        property_details_page.select_house_type(house_type)
        property_details_page.select_storeys(storeys)
        property_details_page.select_extension_exists(extension_exists)
        property_details_page.select_plans_extension(plans_extension)
        property_details_page.uncheck_photo_checkbox()
        property_details_page.upload_photo(test_image_path)
        property_details_page.click_next()

        # Verify confirmation text
        assert property_details_page.is_confirmation_visible(), (
            "Confirmation text not visible after property details submission"
        )

    def test_full_booking_flow(
        self,
        page,
        home_page,
        property_details_page,
        contact_info_page,
        booking_page,
        test_image_path,
    ):
        """
        Test the complete booking flow for Home Energy Assessment.

        Steps:
        1. Navigate: Home -> Our Services -> Home Energy Assessment -> Book
        2. Fill property details (house type, storeys, extensions, upload photo)
        3. Verify confirmation message
        4. Fill contact information (name, email, mobile, address)
        5. Select available date (current month preferred, else next month)
        6. Select time slot
        7. Click Later and verify email confirmation
        """
        # Store email for final assertion
        test_email = TEST_DATA["email"]

        # ========== STEP 1: Navigate to booking ==========
        print("\n[STEP 1] Navigating to Home Energy Assessment booking...")
        home_page.navigate_to_booking()

        # ========== STEP 2: Fill property details ==========
        print("\n[STEP 2] Filling property details...")

        # Select House Type = Semi-detached
        property_details_page.select_house_type(TEST_DATA["house_type"])
        print(f"  - Selected house type: {TEST_DATA['house_type']}")

        # Select No. of Storeys = 2
        property_details_page.select_storeys(TEST_DATA["storeys"])
        print(f"  - Selected storeys: {TEST_DATA['storeys']}")

        # Select Existing extension = Yes
        property_details_page.select_extension_exists(TEST_DATA["extension_exists"])
        print(f"  - Existing extension: {'Yes' if TEST_DATA['extension_exists'] else 'No'}")

        # Select Plans to add extensions = No
        property_details_page.select_plans_extension(TEST_DATA["plans_extension"])
        print(f"  - Plans to extend: {'Yes' if TEST_DATA['plans_extension'] else 'No'}")

        # Uncheck "I don't have a photo"
        property_details_page.uncheck_photo_checkbox()
        print("  - Unchecked 'I don't have a photo'")

        # Upload a photo
        property_details_page.upload_photo(test_image_path)
        print(f"  - Uploaded photo: {test_image_path}")

        # Click Next
        property_details_page.click_next()
        print("  - Clicked Next")

        # ========== STEP 3: Verify confirmation text ==========
        print("\n[STEP 3] Verifying confirmation message...")
        confirmation_text = "Your first step to a warm, comfortable, and healthy home"
        assert property_details_page.is_confirmation_visible(), (
            f"Expected confirmation text '{confirmation_text}' not visible"
        )
        print(f"  - Confirmed: '{confirmation_text}' is visible")

        # Close any popups
        property_details_page.close_popup_if_exists()
        print("  - Closed any popups if present")

        # Click Next to proceed to contact info
        property_details_page.click_next()
        print("  - Clicked Next to proceed to contact info")

        # ========== STEP 4: Fill contact information ==========
        print("\n[STEP 4] Filling contact information...")

        contact_info_page.fill_first_name(TEST_DATA["first_name"])
        print(f"  - First name: {TEST_DATA['first_name']}")

        contact_info_page.fill_last_name(TEST_DATA["last_name"])
        print(f"  - Last name: {TEST_DATA['last_name']}")

        contact_info_page.fill_email(test_email)
        print(f"  - Email: {test_email}")

        contact_info_page.fill_mobile(TEST_DATA["mobile"])
        print(f"  - Mobile: {TEST_DATA['mobile']}")

        # Search for Dublin in address
        contact_info_page.search_address(TEST_DATA["address_search"])
        print(f"  - Searched address: {TEST_DATA['address_search']}")

        # Select from dropdown
        contact_info_page.select_address_from_dropdown()
        print("  - Selected address from dropdown")

        # Click Next
        contact_info_page.click_next()
        print("  - Clicked Next to proceed to booking")

        # ========== STEP 5: Select date ==========
        print("\n[STEP 5] Selecting booking date...")
        current_month = datetime.now().strftime("%B %Y")
        print(f"  - Current month: {current_month}")

        # Try to find available date in current month
        date_selected = booking_page.select_available_date(prefer_current_month=True)

        if date_selected:
            print("  - Selected date in current month")
        else:
            # Navigate to next month and select
            booking_page.navigate_to_next_month()
            booking_page.select_available_date(prefer_current_month=False)
            next_month = datetime.now().strftime("%B %Y")
            print(f"  - Selected date in next month: {next_month}")

        # ========== STEP 6: Select time slot ==========
        print("\n[STEP 6] Selecting time slot...")
        time_selected = booking_page.select_available_time(TEST_DATA["time_preference"])

        if time_selected:
            print(f"  - Selected {TEST_DATA['time_preference']} time slot")
        else:
            # Try any available slot
            booking_page.select_available_time("any")
            print("  - Selected any available time slot")

        # ========== STEP 7: Click Later and verify email ==========
        print("\n[STEP 7] Clicking Later and verifying email...")
        booking_page.click_later()
        print("  - Clicked Later")

        # Assert email is displayed
        email_displayed = booking_page.is_email_displayed(test_email)
        assert email_displayed, (
            f"Expected email '{test_email}' not found in confirmation"
        )
        print(f"  - Verified: Email '{test_email}' is displayed in confirmation")

        print("\n" + "=" * 60)
        print("TEST PASSED: Complete booking flow successful!")
        print("=" * 60)

    def test_email_confirmation(
        self,
        page,
        home_page,
        property_details_page,
        contact_info_page,
        booking_page,
        test_image_path,
    ):
        """Test that email confirmation shows correct email address."""
        # Execute booking flow
        home_page.navigate_to_booking()

        property_details_page.fill_property_details(
            house_type=TEST_DATA["house_type"],
            storeys=TEST_DATA["storeys"],
            extension_exists=TEST_DATA["extension_exists"],
            plans_extension=TEST_DATA["plans_extension"],
            photo_path=test_image_path,
        )

        contact_info_page.fill_contact_info(
            first_name=TEST_DATA["first_name"],
            last_name=TEST_DATA["last_name"],
            email=TEST_DATA["email"],
            mobile=TEST_DATA["mobile"],
            address=TEST_DATA["address_search"],
        )

        booking_page.book_slot(
            prefer_current_month=True,
            time_preference=TEST_DATA["time_preference"],
        )
        booking_page.click_later()

        # Verify email
        displayed_email = booking_page.get_confirmation_email()
        assert TEST_DATA["email"].lower() in displayed_email.lower(), (
            f"Email mismatch: expected '{TEST_DATA['email']}', got '{displayed_email}'"
        )
