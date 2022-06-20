# -*- coding: UTF-8 -*-

import datetime
import re


# ---------------------------------------------------------------------------#
# Helper Function                                                            #
# ---------------------------------------------------------------------------#

# date / time helpers

def current_dt():
    cdt = datetime.datetime.now()
    return cdt


def today_string():
    today = datetime.datetime.today()
    return today.strftime('%d %b %Y')


def tomorrow():
    return datetime.datetime.now() + datetime.timedelta(days=1)


def current_year():
    return int(datetime.date.today().year)


def current_month():
    return int(datetime.date.today().month)


def max_value_next_year():
    return int(current_year() + 1)


def parse_date(input, default=1):
    # https://github.com/acdh-oeaw/mmp/blob/master/archiv/utils.py
    dates = (re.findall(r'\d+', input), input)[0]
    try:
        date_str = dates[0]
    except IndexError:
        date_str = default
    try:
        out = int(date_str)
    except (ValueError, TypeError):
        out = default
    return out


def cent_from_year(year):
    """
    takes an integer and returns the matching century
    """
    # https://github.com/acdh-oeaw/mmp/blob/master/archiv/utils.py
    if year == 0:
        return 1
    elif year < 0:
        return -(year - 1) // -100
    else:
        return (year - 1) // 100 + 1


# obfuscate data

def obfuscate_string(value, cutoff):
    if not value:
        return ""
    text_string = str(value)
    text_string_len = len(text_string)
    cutoff = cutoff
    return text_string[:cutoff] + "." * (text_string_len - cutoff)


def obfuscate_email(value):
    email_address = str(value)
    if "@" not in str(email_address):
        return obfuscate_string(email_address, 3)
    local_part, domain = str(email_address).split("@")
    return "{}...@{}".format(local_part[:1], domain)
