import os

import pomace


URL = "https://www.donaldjtrump.com/landing/the-official-2020-strategy-survey"


def main():
    submits = 0
    errors = 0

    while errors < 10:
        page = pomace.visit(URL)

        page.click_stronger()
        page.click_reelected()
        page.click_mainstream()
        page.click_media()
        page.click_message()
        page.click_twitter()
        page.click_vote()

        person = pomace.fake.person
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email(person.email)
        page.fill_zip(person.zip)

        result = page.click_record_my_vote()
        if "has officially launched" in result:
            submits += 1
            errors = 0
            print(f"Submission count: {submits}")
        else:
            errors += 1

        if submits >= 100 and "CI" in os.environ:
            break
