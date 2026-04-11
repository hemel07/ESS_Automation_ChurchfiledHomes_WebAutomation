"""Debug script to explore tab structure and Contact form."""
from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Go to the assessment page
    print("Navigating to assessment page...")
    page.goto("http://52.49.147.125:3005/one-stop-shop-service/home-energy-assessment/home-energy-assessment-calculator")
    time.sleep(3)

    # Accept cookies
    print("Accepting cookies...")
    try:
        cookie_accept_selectors = [
            'button:has-text("Accept")',
            'button:has-text("Accept All")',
            'button:has-text("Allow")',
            '[data-cookie="accept"]',
            '#cookie-accept',
            '.cookie-accept',
        ]
        for sel in cookie_accept_selectors:
            try:
                btn = page.locator(sel).first
                if btn.is_visible(timeout=2000):
                    print(f"Found cookie accept button: {sel}")
                    btn.click()
                    time.sleep(1)
                    break
            except:
                continue
    except Exception as e:
        print(f"Cookie handling: {e}")

    # Fill house type
    print("\n=== Filling House Type ===")
    page.get_by_text("Semi-Detached").first.click()
    time.sleep(0.5)

    # Fill storeys
    print("Filling Storeys...")
    page.get_by_text("2 Storeys").first.click()
    time.sleep(0.5)

    # Extension exists - Yes
    print("Filling Extension...")
    page.get_by_text("Yes").all()[0].click()
    time.sleep(0.5)

    # Plans extension - No
    print("Filling Plans Extension...")
    page.get_by_text("No").all()[0].click()
    time.sleep(0.5)

    # Uncheck photo checkbox
    print("Unchecking photo...")
    try:
        photo_label = page.get_by_text("I don't have a photo to hand").first
        photo_label.click()
    except:
        pass
    time.sleep(0.5)

    # Upload photo
    print("Uploading photo...")
    os.makedirs("test_data", exist_ok=True)
    png_header = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
        0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
        0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,
        0x54, 0x08, 0xD7, 0x63, 0xF8, 0xFF, 0xFF, 0x3F,
        0x00, 0x05, 0xFE, 0x02, 0xFE, 0xDC, 0xCC, 0x59,
        0xE7, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E,
        0x44, 0xAE, 0x42, 0x60, 0x82,
    ])
    with open("test_data/test_image.png", "wb") as f:
        f.write(png_header)
    page.locator('input[type="file"]').first.set_input_files("test_data/test_image.png")
    time.sleep(1)

    # Close modal if exists
    print("Checking for modal after form submission...")
    try:
        modal = page.locator('.app-modal.open, div.modal.show').first
        if modal.is_visible(timeout=3000):
            print("Modal found, looking for close button...")
            # Try various close selectors
            close_selectors = [
                '.app-modal-close',
                'button[aria-label="Close"]',
                '.close-modal',
                'button:has-text("Close")',
                'button:has-text("X")',
                '.modal-header button',
            ]
            for sel in close_selectors:
                try:
                    close_btn = page.locator(sel).first
                    if close_btn.is_visible(timeout=1000):
                        print(f"Found close button: {sel}")
                        close_btn.click()
                        time.sleep(1)
                        break
                except:
                    continue
    except Exception as e:
        print(f"No modal or error: {e}")

    # Click Next first time - shows confirmation
    print("Clicking Next (first time)...")
    page.get_by_text("Next", exact=True).first.click()
    time.sleep(3)

    print(f"\nAfter first Next - URL: {page.url}")

    # Look for confirmation text
    print("\n=== Looking for confirmation text ===")
    if page.get_by_text("Your first step to a warm, comfortable, and healthy home").is_visible(timeout=2000):
        print("Confirmation text is visible!")

    # Click Next second time to go to Contact
    print("\n=== Clicking Next (second time) to go to Contact ===")
    page.get_by_text("Next", exact=True).first.click()
    time.sleep(3)

    print(f"After second Next - URL: {page.url}")

    # Look for all inputs again
    print("\n=== All inputs after second Next ===")
    inputs = page.locator('input').all()
    for i, inp in enumerate(inputs[:20]):
        try:
            if inp.is_visible(timeout=500):
                inp_type = inp.get_attribute('type') or 'N/A'
                inp_name = inp.get_attribute('name') or 'N/A'
                inp_id = inp.get_attribute('id') or 'N/A'
                placeholder = inp.get_attribute('placeholder') or 'N/A'
                print(f"  [{i}] type={inp_type} name={inp_name} id={inp_id} placeholder={placeholder[:30] if placeholder else 'N/A'}")
        except:
            pass

    # Look for all visible text that might be labels
    print("\n=== All visible text that might be form labels ===")
    all_text = page.locator('span, div, p, label').all()
    for i, el in enumerate(all_text[:100]):
        try:
            if el.is_visible(timeout=300):
                text = el.inner_text().strip()
                if text and len(text) < 50:
                    if any(kw in text.lower() for kw in ['first', 'last', 'name', 'email', 'mobile', 'phone', 'address', 'property', 'contact']):
                        print(f"  [{i}] '{text}'")
        except:
            pass

    # Look for tab content containers
    print("\n=== Tab content containers ===")
    tab_contents = page.locator('[class*="tab-content"], [id*="tab-content"], .tab-pane, [role="tabpanel"]').all()
    for i, tc in enumerate(tab_contents[:10]):
        try:
            if tc.is_visible(timeout=500):
                text = tc.inner_text()[:200]
                print(f"  [{i}] Visible: {text}")
        except:
            pass

    # Try to find Contact section by looking for "Contact" text
    print("\n=== Elements near 'Contact' text ===")
    try:
        contact_text = page.get_by_text("Contact").all()
        for i, ct in enumerate(contact_text[:5]):
            try:
                if ct.is_visible(timeout=500):
                    print(f"  [{i}] 'Contact' found")
                    parent = ct.locator("..")
                    print(f"      Parent class: {parent.get_attribute('class') if parent else 'N/A'}")
                    # Look for inputs inside parent
                    inputs_in_parent = parent.locator('input').all()
                    for j, inp in enumerate(inputs_in_parent[:5]):
                        try:
                            if inp.is_visible(timeout=500):
                                inp_name = inp.get_attribute('name') or 'N/A'
                                inp_type = inp.get_attribute('type') or 'N/A'
                                print(f"      Input [{j}]: name={inp_name} type={inp_type}")
                        except:
                            pass
            except:
                pass
    except Exception as e:
        print(f"Error: {e}")

    browser.close()
