"""Debug script to explore react-select dropdown structure."""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Go directly to the assessment page
    print("Navigating to assessment page...")
    page.goto("http://52.49.147.125:3005/one-stop-shop-service/home-energy-assessment/home-energy-assessment-calculator")
    time.sleep(3)

    # Look for House Type text and what's around it
    print("\n=== Looking near 'House Type' ===")
    try:
        house_type_el = page.locator('text=House Type').first
        if house_type_el.is_visible():
            print("Found 'House Type' text")
            parent = house_type_el.locator("..")
            print(f"Parent HTML: {parent.inner_html()[:500]}")

            # Look for what comes after
            next_sibling = house_type_el.locator("xpath=following-sibling::*[1]")
            print(f"Next sibling: {next_sibling.inner_text()[:200] if next_sibling else 'N/A'}")
    except Exception as e:
        print(f"Error: {e}")

    # Look at the input field
    print("\n=== The input field ===")
    try:
        inp = page.locator('#react-select-2-input').first
        if inp.is_visible():
            print(f"Input visible: {inp.is_visible()}")
            inp.click()
            time.sleep(1)

            # Look for options now
            print("\n=== Options ===")
            opts = page.locator('div[id*="react-select"][id*="option"]').all()
            print(f"Found {len(opts)} options")
            for i, opt in enumerate(opts[:10]):
                try:
                    if opt.is_visible(timeout=500):
                        print(f"  [{i}] {opt.inner_text()}")
                except:
                    pass
        else:
            print("Input not visible")
    except Exception as e:
        print(f"Input error: {e}")

    # Try filling the input directly
    print("\n=== Trying to type in input ===")
    try:
        inp = page.locator('input[id*="react-select"]').first
        inp.fill("Semi")
        time.sleep(1)

        # Look for options with text
        opts = page.locator('[role="option"]').all()
        print(f"After typing, found {len(opts)} options")
        for i, opt in enumerate(opts[:10]):
            try:
                if opt.is_visible(timeout=500):
                    print(f"  [{i}] {opt.inner_text()}")
            except:
                pass
    except Exception as e:
        print(f"Fill error: {e}")

    browser.close()
