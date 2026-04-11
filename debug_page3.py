"""Debug script to find modal close button."""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Go to homepage
    print("Navigating to homepage...")
    page.goto("http://52.49.147.125:3005/")
    time.sleep(3)

    # Check for modal
    print("\n=== Checking for modal ===")
    modals = page.locator('.app-modal, .modal, [role="dialog"]').all()
    print(f"Found {len(modals)} modals")

    # Look for close buttons
    print("\n=== Looking for close buttons ===")
    close_buttons = page.locator('button, a').all()
    for i, btn in enumerate(close_buttons[:50]):
        try:
            if btn.is_visible(timeout=1000):
                text = btn.inner_text().strip()
                if text and ('close' in text.lower() or 'x' in text.lower() or '×' in text):
                    print(f"  [{i}] '{text}'")
        except:
            pass

    # Look for buttons with aria-label
    print("\n=== Buttons with aria-label ===")
    aria_buttons = page.locator('[aria-label]').all()
    for btn in aria_buttons:
        try:
            if btn.is_visible(timeout=1000):
                label = btn.get_attribute('aria-label')
                print(f"  - {label}")
        except:
            pass

    # Check for image close buttons
    print("\n=== All images (might be close icons) ===")
    images = page.locator('img').all()
    for i, img in enumerate(images[:20]):
        try:
            if img.is_visible(timeout=1000):
                alt = img.get_attribute('alt')
                src = img.get_attribute('src')
                if alt or ('close' in str(src).lower() or 'x' in str(src).lower()):
                    print(f"  [{i}] alt='{alt}', src='{src[:50]}...'")
        except:
            pass

    # Try clicking with keyboard
    print("\n=== Trying ESC key to close modal ===")
    page.keyboard.press('Escape')
    time.sleep(1)

    # Now try clicking Our Services
    print("\n=== Trying to click Our Services ===")
    try:
        page.locator('a:has-text("Our Services")').first.click()
        print("Success!")
        time.sleep(3)
    except Exception as e:
        print(f"Failed: {e}")

    browser.close()
