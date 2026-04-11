"""Debug script to explore page structure after clicking Our Services."""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Go to homepage
    print("Navigating to homepage...")
    page.goto("http://52.49.147.125:3005/")
    time.sleep(2)

    # Click Our Services
    print("\nClicking Our Services...")
    page.locator('a:has-text("Our Services")').first.click()
    time.sleep(3)

    # Check if dropdown appeared or page navigated
    print(f"\nCurrent URL: {page.url}")

    # Check for visible Home Energy Assessment links
    print("\n=== Looking for visible 'Home Energy Assessment' links ===")
    all_energy_links = page.locator('a:has-text("Home Energy Assessment")').all()
    print(f"Found {len(all_energy_links)} total links")
    for i, link in enumerate(all_energy_links):
        try:
            is_visible = link.is_visible()
            print(f"  [{i}] visible={is_visible}")
            if is_visible:
                box = link.bounding_box()
                print(f"      Box: {box}")
        except Exception as e:
            print(f"  [{i}] Error: {e}")

    # Try to click the first one (even if hidden, scroll first)
    print("\n=== Attempting to click Home Energy Assessment ===")
    target = page.locator('a:has-text("Home Energy Assessment")').first
    try:
        target.scroll_into_view_if_needed()
        time.sleep(1)
        target.click()
        print("Clicked successfully!")
        time.sleep(3)
        print(f"New URL: {page.url}")
    except Exception as e:
        print(f"Click failed: {e}")

    browser.close()
