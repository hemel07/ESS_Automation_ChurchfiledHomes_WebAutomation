# Test Run Log

> This file is automatically updated on each test run.

## Latest Run

**Run Date:** 2026-04-11 21:45:12
**Status:** ❌ Failed
**Total Tests:** 5
**Passed:** 2
**Failed:** 3
**Skipped:** 0
**Duration:** 0:10:45

---

## Run History

| Date | Status | Passed | Failed | Skipped | Duration |
|------|--------|--------|--------|---------|----------|
| 2026-04-11 21:45:12 | ❌ Failed | 2 | 3 | 0 | 0:10:45 |

---

## Test Details

### ✅ Passed Tests
- `test_property_details_form[semi_2storey_ext]`
- `test_property_details_form[detached_2storey_noext]`

### ❌ Failed Tests
- `test_property_details_form[terraced_1storey_planext]`
  ```
  self = <tests.test_booking_flow.TestHomeEnergyAssessmentBooking object at 0x10c68dba0>
page = <Page url='http://52.49.147.125:3005/one-stop-shop-service/home-energy-assessment/home-energy-assessment-calculator#tab-header'>
home_page = <pages.home_page.HomePage object at 0x10cfe6990>
property_details_page = <pages.property_details_page.PropertyDetailsPage object at 0x10cfe6ad0>, house_type = 'Terraced'
storeys = '1', extension_exists = True, plans_extension = True
test_image_path = '/Users/hemels...
  ```
- `test_full_booking_flow`
  ```
  self = <tests.test_booking_flow.TestHomeEnergyAssessmentBooking object at 0x10c68e190>
page = <Page url='http://52.49.147.125:3005/one-stop-shop-service/home-energy-assessment/home-energy-assessment-calculator#tab-header'>
home_page = <pages.home_page.HomePage object at 0x10cd5b950>
property_details_page = <pages.property_details_page.PropertyDetailsPage object at 0x10cd5ba80>
contact_info_page = <pages.contact_info_page.ContactInfoPage object at 0x10ca1aba0>
booking_page = <pages.booking_page.B...
  ```
- `test_email_confirmation`
  ```
  self = <tests.test_booking_flow.TestHomeEnergyAssessmentBooking object at 0x10c6939b0>
page = <Page url='http://52.49.147.125:3005/one-stop-shop-service/home-energy-assessment/home-energy-assessment-calculator#tab-header'>
home_page = <pages.home_page.HomePage object at 0x10e112060>
property_details_page = <pages.property_details_page.PropertyDetailsPage object at 0x10e112190>
contact_info_page = <pages.contact_info_page.ContactInfoPage object at 0x10d4b3750>
booking_page = <pages.booking_page.B...
  ```


---

*Last updated: 2026-04-11 21:45:12*
