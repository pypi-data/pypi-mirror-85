import random

import pomace
import zipcodes

URL = "https://unlockmichigan.ivolunteers.com/Register/extrapetitions"


def main():
    submits = 0
    errors = 0

    while errors < 10:
        page = pomace.visit(URL)

        person = pomace.fake.person
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email(person.email)

        place = get_random_place()
        page.fill_address(place["address"])
        page.fill_city(place["city"])
        page.select_state(place["state"])
        page.fill_zip_code(place["zip_code"])

        result = page.click_sign_up()

        if "Thanks for joining our drive" in result:
            submits += 1
            errors = 0
            print(f"Submission count: {submits}")
        else:
            errors += 1
            print(f"Error count: {errors}")


def get_random_place():
    place = random.choice(zipcodes.filter_by(state="MI"))
    number = random.randint(50, 200)
    street = random.choice(["First", "Second", "Third", "Fourth", "Park", "Main"])
    address = f"{number} {street} St."
    if random.random() < 0.75:
        place["address"] = address
    else:
        place["address"] = pomace.fake.street_address
    return place

