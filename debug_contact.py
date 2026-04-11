"""Debug script to explore contact form structure."""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Go directly to the assessment page
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
    page.get_by_text("Yes").all()[0].click()  # First Yes is for extension
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
    page.locator('input[type="file"]').first.set_input_files("test_data/test_image.png")
    time.sleep(1)

    # Click Next
    print("Clicking Next...")
    page.get_by_text("Next", exact=True).first.click()
    time.sleep(3)

    print(f"\nCurrent URL: {page.url}")

    # Look for form fields
    print("\n=== Looking for contact form fields ===")
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

    # Look for labels
    print("\n=== Labels ===")
    labels = page.locator('label').all()
    for i, lbl in enumerate(labels[:10]):
        try:
            if lbl.is_visible(timeout=500):
                text = lbl.inner_text().strip()
                if text:
                    print(f"  [{i}] '{text[:50]}'")
        except:
            pass

    # Try to find First Name field
    print("\n=== Looking for 'First Name' ===")
    first_name_els = page.locator('[name="firstName"], [placeholder*="First"], text=First Name').all()
    print(f"Found {len(first_name_els)} elements")
    for i, el in enumerate(first_name_els):
        try:
            is_visible = el.is_visible()
            print(f"  [{i}] visible={is_visible}")
            if is_visible:
                box = el.bounding_box()
                print(f"      box: {box}")
        except Exception as e:
            print(f"  [{i}] Error: {e}")

    browser.close()
