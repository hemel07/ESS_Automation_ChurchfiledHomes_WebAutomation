# Test Run Log

> This file is automatically updated on each test run.

## Latest Run

**Run Date:** 2026-04-19 19:22:12
**Status:** ❌ Failed
**Total Tests:** 5
**Passed:** 2
**Failed:** 3
**Skipped:** 0
**Duration:** 0:19:52

---

## Run History

| Date | Status | Passed | Failed | Skipped | Duration |
|------|--------|--------|--------|---------|----------|
| 2026-04-19 19:22:12 | ❌ Failed | 2 | 3 | 0 | 0:19:52 |

---

## Test Details

### ✅ Passed Tests
- `test_property_details_form[semi_2storey_ext]`
- `test_property_details_form[detached_2storey_noext]`

### ❌ Failed Tests
- `test_property_details_form[terraced_1storey_planext]`
  ```
  self = <tests.test_booking_flow.TestHomeEnergyAssessmentBooking object at 0x1107adcd0>
page = <Page url='http://52.49.147.125:3005/one-stop-shop-service/home-energy-assessment/home-energy-assessment-calculator#tab-header'>
home_page = <pages.home_page.HomePage object at 0x11112a990>
property_details_page = <pages.property_details_page.PropertyDetailsPage object at 0x11112aad0>
house_type = 'Terraced', storeys = '1', extension_exists = True, plans_extension = True
test_image_path = '/Users/hemels...
  ```
- `test_full_booking_flow`
  ```
  self = <tests.test_booking_flow.TestHomeEnergyAssessmentBooking object at 0x1107ae2c0>
page = <Page url='http://52.49.147.125:3005/one-stop-shop-service/home-energy-assessment/home-energy-assessment-calculator#tab-header'>
home_page = <pages.home_page.HomePage object at 0x110e83820>
property_details_page = <pages.property_details_page.PropertyDetailsPage object at 0x110e83950>
contact_info_page = <pages.contact_info_page.ContactInfoPage object at 0x110b46e40>
booking_page = <pages.booking_page.B...
  ```
- `test_email_confirmation`
  ```
  self = <tests.test_booking_flow.TestHomeEnergyAssessmentBooking object at 0x1107b39b0>
page = <Page url='http://52.49.147.125:3005/one-stop-shop-service/home-energy-assessment/home-energy-assessment-calculator#tab-header'>
home_page = <pages.home_page.HomePage object at 0x111717360>
property_details_page = <pages.property_details_page.PropertyDetailsPage object at 0x111717490>
contact_info_page = <pages.contact_info_page.ContactInfoPage object at 0x1115a7610>
booking_page = <pages.booking_page.B...
  ```


---

*Last updated: 2026-04-19 19:22:12*
