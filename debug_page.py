"""Debug script to explore page structure."""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Go to homepage
    print("Navigating to homepage...")
    page.goto("http://52.49.147.125:3005/")
    time.sleep(3)

    # Find "Our Services" and click
    print("\n=== Looking for 'Our Services' ===")
    our_services = page.get_by_text("Our Services").all()
    print(f"Found {len(our_services)} elements with 'Our Services'")
    for i, el in enumerate(our_services):
        if el.is_visible():
            print(f"  [{i}] {el.inner_text()[:50]}")
            try:
                print(f"      Tag: {el.evaluate('el => el.tagName')}")
                print(f"      Class: {el.evaluate('el => el.className')}")
            except:
                pass

    # Click first Our Services
    page.get_by_text("Our Services").first.click()
    time.sleep(3)

    print("\n=== After clicking Our Services - Looking for Home Energy Assessment ===")
    # List all clickable text elements
    all_links = page.locator('a').all()
    print(f"Found {len(all_links)} links")
    for i, link in enumerate(all_links[:20]):  # First 20
        try:
            if link.is_visible():
                text = link.inner_text().strip()
                if text and len(text) < 100:
                    print(f"  [{i}] {text}")
        except:
            pass

    # Look for energy/assessment related
    energy_links = page.locator('a:has-text("Energy"), a:has-text("Assessment"), a:has-text("energy"), a:has-text("assessment")').all()
    print(f"\nFound {len(energy_links)} energy/assessment links")
    for i, link in enumerate(energy_links):
        try:
            if link.is_visible():
                text = link.inner_text().strip()
                print(f"  [{i}] {text}")
        except:
            pass

    # Get page content
    print("\n=== Page Title ===")
    print(page.title())

    print("\n=== Current URL ===")
    print(page.url)

    browser.close()
