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

    # Close modal first
    print("Closing modal...")
    try:
        page.locator('button[aria-label="Close"]').first.click()
        time.sleep(1)
    except:
        pass

    # Click Our Services
    print("\nClicking Our Services...")
    page.locator('a:has-text("Our Services")').first.click()
    time.sleep(3)

    print(f"\nCurrent URL: {page.url}")

    # Check for dropdown menu
    print("\n=== Looking for dropdown/submenu ===")
    dropdowns = page.locator('.dropdown, .submenu, [class*="dropdown"], [class*="menu"]').all()
    print(f"Found {len(dropdowns)} dropdowns")

    # Check all visible links after clicking
    print("\n=== All visible links after click ===")
    all_links = page.locator('a').all()
    for i, link in enumerate(all_links):
        try:
            if link.is_visible(timeout=500):
                text = link.inner_text().strip()
                if text and len(text) < 80:
                    # Check if it's in viewport
                    box = link.bounding_box()
                    print(f"  [{i}] '{text[:50]}' - visible, box: y={box['y'] if box else 'N/A'}")
        except:
            pass

    # Look for Home Energy Assessment specifically
    print("\n=== Looking for 'Home Energy Assessment' ===")
    hea_links = page.locator('a:has-text("Home Energy Assessment")').all()
    print(f"Found {len(hea_links)} links")
    for i, link in enumerate(hea_links):
        try:
            is_visible = link.is_visible()
            print(f"  [{i}] visible={is_visible}")
            if is_visible:
                box = link.bounding_box()
                print(f"      box: {box}")
                # Try clicking
                link.click()
                print("      Clicked!")
                time.sleep(3)
                print(f"      New URL: {page.url}")
                break
        except Exception as e:
            print(f"      Error: {e}")

    browser.close()
