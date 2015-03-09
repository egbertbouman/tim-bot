import sys
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
        
    def goto_week(self, week_no=0):
        i = week_no - self._get_week()
        while i != 0:
            if i > 0:
                self._goto_next_week()
            else:
                self._goto_prev_week()
            i = week_no - self._get_week()
    
    def _goto_next_week(self):
        elem = self.browser.find_element_by_css_selector('img[src="https://hours.tudelft.nl/img/nextweek.gif"]')
        elem.click()
        
    def _goto_prev_week(self):
        elem = self.browser.find_element_by_css_selector('img[src="https://hours.tudelft.nl/img/prevweek.gif"]')
        elem.click()
    
    def _goto_curr_week(self):
        elem = self.browser.find_element_by_css_selector('img[src="https://hours.tudelft.nl/img/currweek.gif"]')
        elem.click()
        
    def _get_week(self):
        return int(self.browser.find_element_by_css_selector('td.msheetcontextCol2 > strong').text.split()[-1])

    def close(self):
        self.browser.close()

def main(argv):
    parser = argparse.ArgumentParser(add_help=False, description=('Automate the process of filling in hour-registration in TIM'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
    parser.add_argument('--username', '-u', help='NetID username for logging into TIM')
    parser.add_argument('--password', '-p', help='NetID password')
    parser.add_argument('--firefox', '-f', help='Location of Firefox executable')

    try:
        args = parser.parse_args(sys.argv[1:])

        username = args.username
        password = args.password

        if not username or not password:
            parser.print_usage()
            raise ValueError('username and password are required options')

        tim = TimBot(username, password, args.firefox)
        tim.goto_week(1)

    except Exception, e:
        print 'Error:', str(e)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])

