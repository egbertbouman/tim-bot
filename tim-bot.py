import sys
import getpass
import argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class TimBot(object):

    TIM_URL = 'https://hours.tudelft.nl/web'

    def __init__(self, username, password, binary=None):
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(binary) if binary else None)
        self.browser.get(TimBot.TIM_URL)
        assert "TimEnterprise Web client" in self.browser.title

        # Login
        elem = self.browser.find_element_by_name("fusername")
        elem.send_keys(username)
        elem = self.browser.find_element_by_name("fpassword")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)

        # TODO: check if logged in

    def goto_tab(self, name):
        for elem in self.browser.find_elements_by_css_selector('.Tab > a'):
            if elem.text == name:
                elem.click()
                break

    def goto_menu(self, name):
        for elem in self.browser.find_elements_by_css_selector('.menuitemtxtcell .menuitemlink'):
            if elem.text == name:
                elem.click()
                break

    def goto_week(self, week_no=0):
        # Goto current week
        if week_no == 0:
            elem = self.browser.find_element_by_css_selector('img[src="https://hours.tudelft.nl/img/currweek.gif"]')
            elem.click()

        i = week_no - self._get_week()
        while i != 0:
            selector = 'img[src="https://hours.tudelft.nl/img/%s.gif"]' % ('nextweek'if i > 0 else 'prevweek')
            elem = self.browser.find_element_by_css_selector(selector)
            elem.click()
            i = week_no - self._get_week()

    def _get_week(self):
        return int(self.browser.find_element_by_css_selector('td.msheetcontextCol2 > strong').text.split()[-1])

    def set_hours(self, value, product_code='IAOU'):
        for elem in self.browser.find_elements_by_css_selector('td[class^="mrh"][class*="bc"] > span[class="mdisspan"]'):
            if elem.text == product_code:
                parent = elem.find_element_by_xpath('../..')
                elems = parent.find_elements_by_css_selector('td[class^="mcv"] > div > input')
                for e in elems:
                    e.clear()
                    e.send_keys(value)

    def close(self):
        self.browser.close()


def login_prompt(username=None):
    username = username or raw_input('Username: ')
    password = getpass.getpass('Password: ')
    return username, password


def main(argv):
    parser = argparse.ArgumentParser(add_help=False, description=('Automate the process of filling in hour-registration in TIM'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
    parser.add_argument('--username', '-u', help='NetID username for logging into TIM')
    parser.add_argument('--firefox', '-f', help='Location of Firefox executable')

    try:
        args = parser.parse_args(sys.argv[1:])

        username, password = login_prompt(args.username)
        tim = TimBot(username, password, args.firefox)
        #tim.goto_tab('Calendar')
        tim.goto_week(10)
        tim.set_hours(1)
        #tim.goto_menu('Close TimEnterprise')

    except Exception, e:
        print 'Error:', str(e)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])

