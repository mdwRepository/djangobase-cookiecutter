# -*- coding: UTF-8 -*-

import datetime


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
