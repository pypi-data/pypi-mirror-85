import log
import pomace


URL = "https://reopennc.com"
MAX_ERROR_COUNT = 10


def main():
    page = pomace.visit(URL)
    log.info(f"Launched {URL}")

    success_count = error_count = 0
    while error_count < MAX_ERROR_COUNT:
        page = page.click_home()
        page = page.click_contact_us()

        person = pomace.fake.person
        page.fill_name(f'{person.first_name} {person.last_name}')
        page.fill_email(person.email)
        page.fill_message(fake.paragraph())
        page = page.click_send()

        if "We will get back to you" not in page:
            error_count += 1
            log.error(f"Failed to submit (attempt {error_count})")
            page = pomace.visit(URL, delay=3)
        else:
            success_count += 1
            error_count = 0
            log.info(f"Successful submissions: {success_count}")
