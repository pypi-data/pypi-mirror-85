import time

import pomace


URL = "https://trumpvictory.com/free-yard-sign/"


def main():
    submits = 0
    errors = 0

    while errors < 10:
        page = pomace.visit(URL)

        person = pomace.fake.person
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email_address(person.email_address)
        page.fill_cell_phone(person.cell_phone)
        page.fill_address(person.address)
        page.fill_city(person.city)
        page.select_state(person.state)
        page.fill_zip_code(person.zip_code)

        result = page.click_submit()
        while pomace.shared.browser.url == URL:
            time.sleep(1)  # CAPTCHA visible

        if "Now take the next step" in result:
            submits += 1
            errors = 0
            print(f"Submission count: {submits}")
        else:
            errors += 1
            print(f"Error count: {errors}")
