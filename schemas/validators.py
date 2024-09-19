import re


def validate_phone_number(phone_number: str):
    regex = re.compile(r'^\d{9,15}$')
    return regex.match(phone_number)
