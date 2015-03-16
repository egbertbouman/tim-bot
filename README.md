# tim-bot

Automate the process of hour registration in TimEnterprise.

### Dependencies
* Python 2.7+
* selenium

You can install selenium using pip

    pip install selenium


### Usage
```
usage: tim-bot.py [--help] [--username USERNAME] [--firefox FIREFOX]
                  [--weeks WEEKS] [--codes CODES]

Automate the process of filling in hour-registration in TIM

optional arguments:
  --help, -h            Show this help message and exit
  --username USERNAME, -u USERNAME
                        NetID username for logging into TIM
  --firefox FIREFOX, -f FIREFOX
                        Location of Firefox executable
  --weeks WEEKS, -w WEEKS
                        Weeks for which to fill in hour registration
                        (example: 1-5,8,10)
  --codes CODES, -c CODES
                        Comma-separated list of hours and BAAN-codes,
                        in the form: <hours>@<BAAN-code>
                        (example: 7@CODE1,1@CODE2)
```
