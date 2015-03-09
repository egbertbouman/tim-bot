import sys
import argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TimBot(object):

    TIM_URL = 'https://hours.tudelft.nl/web'

    def __init__(self, username, password, browser='firefox'):
        if browser == 'firefox':
            self.browser = webdriver.Firefox()
        else:
            raise Exception('Unsupported browser')

        self.browser.get(TimBot.TIM_URL)
        assert "TimEnterprise Web client" in self.browser.title

        # Login
        elem = self.browser.find_element_by_name("fusername")
        elem.send_keys(username)
        elem = self.browser.find_element_by_name("fpassword")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)

        # TODO: check if logged in

    def close(self):
        self.browser.close()

def main(argv):
    parser = argparse.ArgumentParser(add_help=False, description=('Automate the process of filling in hour-registration in TIM'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
    parser.add_argument('--username', '-u', help='NetID username for logging into TIM')
    parser.add_argument('--password', '-p', help='NetID password')

    try:
        args = parser.parse_args(sys.argv[1:])

        username = args.username
        password = args.password

        if not username or not password:
            parser.print_usage()
            raise ValueError('username and password are required options')

        tim = TimBot(username, password)

    except Exception, e:
        print 'Error:', str(e)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
