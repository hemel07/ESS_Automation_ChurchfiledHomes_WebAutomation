# ESS Automation - Playwright Pytest Framework

A Page Object Model (POM) based test automation framework for ESS Home Energy Assessment booking flow.

## Project Structure

```
ESS_Automation_hemel/
├── conftest.py           # Pytest fixtures and configuration
├── pytest.ini            # Pytest configuration
├── requirements.txt      # Python dependencies
├── pages/                # Page Object Models
│   ├── __init__.py
│   ├── base_page.py      # Base page with common methods
│   ├── home_page.py      # Home page locators/actions
│   ├── property_details_page.py
│   ├── contact_info_page.py
│   └── booking_page.py
├── tests/                # Test files
│   ├── __init__.py
│   └── test_booking_flow.py
├── test_data/            # Test data files (auto-created)
└── reports/              # HTML test reports (auto-generated)
    └── booking_test_report.html
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_booking_flow.py::TestHomeEnergyAssessmentBooking::test_full_booking_flow

# Run with verbose output
pytest -v

# Run tests in parallel
pytest -n 4

# Generate report (default behavior)
# Report will be saved to reports/booking_test_report.html
```

## Test Coverage

The framework tests the complete Home Energy Assessment booking flow:

1. **Navigation**: Home → Our Services → Home Energy Assessment → Book
2. **Property Details**: House type, storeys, extensions, photo upload
3. **Contact Information**: Name, email, mobile, address search
4. **Booking**: Date selection (current/next month), time slot selection
5. **Confirmation**: Email verification

## Page Object Model

### BasePage
Common methods available to all pages:
- `click()`, `fill()`, `select_dropdown()`
- `is_visible()`, `wait_for_element()`
- `upload_file()`, `close_popup_if_exists()`

### HomePage
- `navigate_to_booking()` - Complete navigation flow
- `click_our_services()`
- `click_home_energy_assessment()`
- `click_book_assessment()`

### PropertyDetailsPage
- `select_house_type()`
- `select_storeys()`
- `select_extension_exists()`
- `select_plans_extension()`
- `uncheck_photo_checkbox()`
- `upload_photo()`

### ContactInfoPage
- `fill_contact_info()`
- `search_address()`
- `select_address_from_dropdown()`

### BookingPage
- `select_available_date()`
- `select_available_time()`
- `click_later()`
- `is_email_displayed()`

## HTML Report

After each test run, an HTML report is automatically generated at:
`reports/booking_test_report.html`

The report includes:
- Test results (pass/fail)
- Execution time
- Error details and stack traces
- Screenshots on failure (if configured)

## Configuration

Edit `pytest.ini` to customize:
- Test paths
- Report location
- Additional pytest options

Edit `conftest.py` to customize:
- Browser settings (headless mode, viewport)
- Base URL
- Fixtures
# ESS_Automation_ChurchfiledHomes_WebAutomation
