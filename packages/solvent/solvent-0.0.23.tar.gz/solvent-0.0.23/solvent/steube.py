import os

import pomace
from pomace import shared

URL = "https://steube.house.gov/contact/newsletter"


def main():
    submits = 0
    errors = 0

    while errors < 10:
        page = pomace.visit(URL)

        person = pomace.fake.person
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email(person.email)

        print("Type word from audio CAPTCHA and click Subscribe...")
        while shared.browser.url == str(page.url):
            pass

        if "thank-you" in shared.browser.url:
            submits += 1
            errors = 0
            print(f"Submission count: {submits}")
        else:
            errors += 1
            print(f"Error count: {errors}")
