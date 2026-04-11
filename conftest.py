import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from pages.home_page import HomePage
from pages.property_details_page import PropertyDetailsPage
from pages.contact_info_page import ContactInfoPage
from pages.booking_page import BookingPage
from datetime import datetime
import os

# Path to the auto-updated test run log
TEST_RUN_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "report.md")

# Store test results for the session
_test_results = {
    "passed": [],
    "failed": [],
    "skipped": [],
    "start_time": None,
    "end_time": None,
}


def pytest_sessionstart(session):
    """Called at the start of the test session."""
    _test_results["start_time"] = datetime.now()


def pytest_runtest_logreport(report):
    """Collect test results as they complete."""
    if report.when == "call":
        if report.passed:
            _test_results["passed"].append(report.nodeid)
        elif report.failed:
            _test_results["failed"].append({
                "nodeid": report.nodeid,
                "error": str(report.longrepr) if report.longrepr else "Unknown error"
            })
    elif report.when == "setup" and report.skipped:
        _test_results["skipped"].append(report.nodeid)


def pytest_sessionfinish(session):
    """Called at the end of the test session - updates the markdown log."""
    _test_results["end_time"] = datetime.now()
    _update_test_run_log()


def _update_test_run_log():
    """Update the reports/report.md file with latest results."""
    start_time = _test_results["start_time"] or datetime.now()
    end_time = _test_results["end_time"] or datetime.now()
    duration = end_time - start_time

    passed_count = len(_test_results["passed"])
    failed_count = len(_test_results["failed"])
    skipped_count = len(_test_results["skipped"])
    total_count = passed_count + failed_count + skipped_count

    # Determine overall status
    if failed_count > 0:
        status = "Failed"
        status_emoji = "❌"
    elif skipped_count > 0 and passed_count == 0:
        status = "Skipped"
        status_emoji = "⏭️"
    elif total_count == 0:
        status = "No Tests Run"
        status_emoji = "⏸️"
    else:
        status = "Passed"
        status_emoji = "✅"

    duration_str = str(duration).split(".")[0]  # Remove microseconds
    run_date = end_time.strftime("%Y-%m-%d %H:%M:%S")

    # Build test details section
    test_details = []

    if _test_results["passed"]:
        test_details.append("### ✅ Passed Tests\n")
        for nodeid in _test_results["passed"]:
            test_name = nodeid.split("::")[-1] if "::" in nodeid else nodeid
            test_details.append(f"- `{test_name}`\n")
        test_details.append("\n")

    if _test_results["failed"]:
        test_details.append("### ❌ Failed Tests\n")
        for result in _test_results["failed"]:
            nodeid = result["nodeid"]
            error = result["error"]
            test_name = nodeid.split("::")[-1] if "::" in nodeid else nodeid
            test_details.append(f"- `{test_name}`\n")
            test_details.append(f"  ```\n  {error[:500]}{'...' if len(error) > 500 else ''}\n  ```\n")
        test_details.append("\n")

    if _test_results["skipped"]:
        test_details.append("### ⏭️ Skipped Tests\n")
        for nodeid in _test_results["skipped"]:
            test_name = nodeid.split("::")[-1] if "::" in nodeid else nodeid
            test_details.append(f"- `{test_name}`\n")
        test_details.append("\n")

    test_details_content = "".join(test_details) if test_details else "_No tests executed._"

    # Read existing history
    history_rows = []
    if os.path.exists(TEST_RUN_LOG_PATH):
        with open(TEST_RUN_LOG_PATH, "r") as f:
            content = f.read()
            # Extract existing history rows
            if "| Date |" in content:
                history_section = content.split("| Date |")[1].split("---")[0].strip()
                for line in history_section.split("\n")[2:]:  # Skip header and separator
                    if line.strip().startswith("|"):
                        history_rows.append(line.strip())

    # Add new row to history (keep last 10 runs)
    new_row = f"| {run_date} | {status_emoji} {status} | {passed_count} | {failed_count} | {skipped_count} | {duration_str} |"
    history_rows.insert(0, new_row)
    history_rows = history_rows[:10]  # Keep only last 10 runs

    history_table = "\n".join(history_rows)

    # Generate new content
    new_content = f"""# Test Run Log

> This file is automatically updated on each test run.

## Latest Run

**Run Date:** {run_date}
**Status:** {status_emoji} {status}
**Total Tests:** {total_count}
**Passed:** {passed_count}
**Failed:** {failed_count}
**Skipped:** {skipped_count}
**Duration:** {duration_str}

---

## Run History

| Date | Status | Passed | Failed | Skipped | Duration |
|------|--------|--------|--------|---------|----------|
{history_table}

---

## Test Details

{test_details_content}
---

*Last updated: {run_date}*
"""

    with open(TEST_RUN_LOG_PATH, "w") as f:
        f.write(new_content)


@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create a new browser context for each test."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Create a new page for each test."""
    page = context.new_page()
    page.goto("http://52.49.147.125:3005/")
    page.set_viewport_size({"width": 1920, "height": 1080})
    yield page


@pytest.fixture
def home_page(page: Page) -> HomePage:
    """Fixture to provide HomePage instance."""
    return HomePage(page)


@pytest.fixture
def property_details_page(page: Page) -> PropertyDetailsPage:
    """Fixture to provide PropertyDetailsPage instance."""
    return PropertyDetailsPage(page)


@pytest.fixture
def contact_info_page(page: Page) -> ContactInfoPage:
    """Fixture to provide ContactInfoPage instance."""
    return ContactInfoPage(page)


@pytest.fixture
def booking_page(page: Page) -> BookingPage:
    """Fixture to provide BookingPage instance."""
    return BookingPage(page)
