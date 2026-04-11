"""Debug script to explore form structure."""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Go directly to the assessment page
    print("Navigating to assessment page...")
    page.goto("http://52.49.147.125:3005/one-stop-shop-service/home-energy-assessment/home-energy-assessment-calculator")
    time.sleep(3)

    # Check for tabs
    print("\n=== Current URL ===")
    print(page.url)

    # Look for form fields
    print("\n=== Looking for House Type field ===")
    labels = page.locator('label').all()
    for i, label in enumerate(labels):
        try:
            if label.is_visible(timeout=500):
                text = label.inner_text().strip()
                if text and ('house' in text.lower() or 'type' in text.lower()):
                    print(f"  Label [{i}]: '{text}'")
                    # Check what's next to this label
                    parent = label.locator("..")
                    print(f"      Parent class: {parent.get_attribute('class')}")
        except:
            pass

    # Look for all inputs
    print("\n=== All inputs/fields ===")
    inputs = page.locator('input, select, textarea').all()
    for i, inp in enumerate(inputs[:30]):
        try:
            if inp.is_visible(timeout=500):
                tag = inp.evaluate('el => el.tagName')
                inp_type = inp.get_attribute('type') or 'N/A'
                inp_name = inp.get_attribute('name') or 'N/A'
                inp_id = inp.get_attribute('id') or 'N/A'
                placeholder = inp.get_attribute('placeholder') or 'N/A'
                print(f"  [{i}] {tag} type={inp_type} name={inp_name} id={inp_id} placeholder={placeholder[:30] if placeholder else 'N/A'}")
        except:
            pass

    # Look for dropdowns (might be custom)
    print("\n=== Looking for custom dropdowns ===")
    dropdowns = page.locator('[class*="dropdown"], [class*="select"], [role="listbox"], [role="combobox"]').all()
    for i, dd in enumerate(dropdowns[:10]):
        try:
            if dd.is_visible(timeout=500):
                print(f"  [{i}] {dd.get_attribute('class')[:80]}")
        except:
            pass

    # Look for radio buttons
    print("\n=== Radio buttons ===")
    radios = page.locator('input[type="radio"]').all()
    for i, radio in enumerate(radios[:10]):
        try:
            if radio.is_visible(timeout=500):
                print(f"  [{i}] name={radio.get_attribute('name')} value={radio.get_attribute('value')}")
        except:
            pass

    # Look for "Next" button
    print("\n=== Next button ===")
    next_btns = page.locator('button:has-text("Next"), a:has-text("Next"), input[value="Next"]').all()
    for i, btn in enumerate(next_btns):
        try:
            if btn.is_visible(timeout=500):
                print(f"  [{i}] {btn.inner_text()[:30]}")
        except:
            pass

    browser.close()
