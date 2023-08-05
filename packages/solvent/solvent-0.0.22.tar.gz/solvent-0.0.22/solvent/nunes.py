import pomace
from selenium.common.exceptions import UnexpectedAlertPresentException


URL = "https://iqconnect.lmhostediq.com/iqextranet/EsurveyForm.aspx?__cid=CA22DN&__sid=100088&__crop=15548.37359788.2764358.1492115"


def main():
    submits = 0
    errors = 0

    while errors < 10:
        page = pomace.visit(URL)

        for index in range(3):
            pomace.shared.browser.find_by_css('[value="Yes"]')[index].click()

        try:
            page.click_submit()
        except UnexpectedAlertPresentException:
            if alert := pomace.shared.browser.get_alert():
                allert.accept()

        if pomace.shared.browser.url == "https://nunes.house.gov/":
            submits += 1
            errors = 0
            print(f"Submission count: {submits}")
        else:
            errors += 1
            print(f"Error count: {errors}")
