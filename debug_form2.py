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

    # Click on first dropdown (House Type)
    print("\n=== Clicking first dropdown ===")
    dropdowns = page.locator('.dropdown').all()
    print(f"Found {len(dropdowns)} dropdowns")

    # Try to click and see options
    for i, dd in enumerate(dropdowns[:5]):
        try:
            if dd.is_visible(timeout=500):
                parent = dd.locator("..")
                parent_text = parent.inner_text()[:100] if parent else "N/A"
                print(f"  [{i}] Parent text: {parent_text}")
        except Exception as e:
            print(f"  [{i}] Error: {e}")

    # Click first dropdown
    try:
        dropdowns[0].click()
        time.sleep(1)

        # Look for options
        print("\n=== Options after click ===")
        options = page.locator('[id*="react-select"], [class*="option"], [role="option"]').all()
        print(f"Found {len(options)} options")
        for i, opt in enumerate(options[:10]):
            try:
                if opt.is_visible(timeout=500):
                    text = opt.inner_text().strip()
                    print(f"  [{i}] {text}")
            except:
                pass
    except Exception as e:
        print(f"Click error: {e}")

    # Look at the input inside dropdown
    print("\n=== Inputs inside dropdowns ===")
    for i, dd in enumerate(dropdowns[:5]):
        try:
            inputs = dd.locator('input').all()
            if inputs:
                print(f"  Dropdown [{i}] has {len(inputs)} input(s)")
        except:
            pass

    # Look for labels
    print("\n=== All visible text that might be labels ===")
    all_text = page.locator('span, div, p').all()
    for i, el in enumerate(all_text):
        try:
            if el.is_visible(timeout=300):
                text = el.inner_text().strip()
                if text and len(text) < 50:
                    if any(kw in text.lower() for kw in ['house', 'type', 'storey', 'extension', 'photo']):
                        print(f"  [{i}] '{text}'")
                        print(f"      Class: {el.get_attribute('class')[:80] if el.get_attribute('class') else 'N/A'}")
        except:
            pass

    browser.close()
