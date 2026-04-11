"""Debug script to explore contact page structure after property details."""
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
    # Create minimal PNG
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
    print("Checking for modal...")
    try:
        modal = page.locator('.app-modal.open').first
        if modal.is_visible(timeout=2000):
            print("Modal found, closing...")
            close_btn = page.locator('.app-modal-close, button[aria-label="Close"], .close-modal').first
            if close_btn.is_visible(timeout=2000):
                close_btn.click()
                time.sleep(1)
    except:
        pass

    # Click Next
    print("Clicking Next...")
    page.get_by_text("Next", exact=True).first.click()
    time.sleep(3)

    # Click on Contact tab
    print("\n=== Clicking Contact tab ===")
    try:
        contact_tab = page.get_by_text("Contact", exact=True).first
        contact_tab.click()
        time.sleep(2)
        print("Clicked Contact tab")
    except Exception as e:
        print(f"Could not click Contact tab: {e}")

    print(f"\nCurrent URL: {page.url}")

    # Check for tabs
    print("\n=== Looking for tabs ===")
    tabs = page.locator('[role="tab"], [class*="tab"], .nav-link, a[class*="nav"]').all()
    for i, tab in enumerate(tabs[:10]):
        try:
            if tab.is_visible(timeout=500):
                text = tab.inner_text().strip()
                print(f"  [{i}] Tab: '{text}'")
        except:
            pass

    # Look for tab-headers specifically
    print("\n=== Looking for tab-headers ===")
    tab_headers = page.locator('[id*="tab"], [class*="tab-header"], .tab-title').all()
    for i, th in enumerate(tab_headers[:10]):
        try:
            if th.is_visible(timeout=500):
                text = th.inner_text().strip()
                print(f"  [{i}] Tab Header: '{text}'")
        except:
            pass

    # Look for all buttons
    print("\n=== All buttons ===")
    buttons = page.locator('button, a.btn').all()
    for i, btn in enumerate(buttons[:20]):
        try:
            if btn.is_visible(timeout=500):
                text = btn.inner_text().strip()[:50]
                print(f"  [{i}] Button: '{text}'")
        except:
            pass

    # Look for all inputs with context
    print("\n=== All inputs with surrounding text ===")
    inputs = page.locator('input').all()
    for i, inp in enumerate(inputs[:20]):
        try:
            if inp.is_visible(timeout=500):
                inp_type = inp.get_attribute('type') or 'N/A'
                inp_name = inp.get_attribute('name') or 'N/A'
                inp_id = inp.get_attribute('id') or 'N/A'
                placeholder = inp.get_attribute('placeholder') or 'N/A'

                # Get parent text
                parent = inp.locator("..")
                parent_text = parent.inner_text()[:100] if parent.is_visible() else "N/A"

                print(f"  [{i}] type={inp_type} name={inp_name} id={inp_id}")
                print(f"       placeholder={placeholder[:30] if placeholder else 'N/A'}")
                print(f"       parent_text={parent_text}")
        except Exception as e:
            print(f"  [{i}] Error: {e}")

    # Look for all labels
    print("\n=== All visible labels ===")
    labels = page.locator('label').all()
    for i, lbl in enumerate(labels[:15]):
        try:
            if lbl.is_visible(timeout=500):
                text = lbl.inner_text().strip()
                if text:
                    print(f"  [{i}] '{text}'")
        except:
            pass

    # Look for all visible text
    print("\n=== All visible text (first 50) ===")
    all_text = page.locator('span, div, p, h1, h2, h3, h4, h5, h6').all()
    for i, el in enumerate(all_text[:50]):
        try:
            if el.is_visible(timeout=300):
                text = el.inner_text().strip()
                if text and len(text) < 100:
                    print(f"  [{i}] '{text}'")
        except:
            pass

    # Check for "Contact Details" or similar section
    print("\n=== Looking for section headers ===")
    headers = page.locator('h1, h2, h3, h4, h5, h6').all()
    for i, h in enumerate(headers):
        try:
            if h.is_visible(timeout=500):
                text = h.inner_text().strip()
                print(f"  [{i}] Header: '{text}'")
        except:
            pass

    # Try to find First Name field specifically
    print("\n=== Trying to find First Name field ===")
    first_name_selectors = [
        'input[name="firstName"]',
        'input[placeholder*="First"]',
        'input[id*="first"]',
        'label:has-text("First") + input',
        'label:has-text("First name") + input',
    ]
    for sel in first_name_selectors:
        try:
            el = page.locator(sel)
            if el.count() > 0:
                visible = el.first.is_visible(timeout=1000)
                print(f"  Selector '{sel}': count={el.count()}, visible={visible}")
        except Exception as e:
            print(f"  Selector '{sel}': Error: {e}")

    browser.close()
