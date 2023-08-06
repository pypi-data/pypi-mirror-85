import os
import random

import pomace


URL = "https://nolabels.salsalabs.org/071020trumphandlingcovid--19/index.html"


def main():
    submits = 0
    errors = 0

    while errors < 10:
        page = pomace.visit(URL)

        page.click_select()
        page.click_no()

        person = pomace.fake.person
        pomace.shared.browser.find_by_text(person.honorific).click()
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email_address(person.email)
        page.fill_zip_code(person.zip)

        page.click_text_messages()

        result = page.click_vote_here()

        if "Log into your Facebook" in result:
            submits += 1
            errors = 0
            print(f"Submission count: {submits}")
        else:
            errors += 1
