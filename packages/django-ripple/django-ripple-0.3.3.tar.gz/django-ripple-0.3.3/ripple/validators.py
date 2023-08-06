import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

from django.core.exceptions import ValidationError


def validate_gb_phone_number(value):
    try:

        parsed = phonenumbers.parse(value, 'GB')
        valid = phonenumbers.is_valid_number(parsed)
    except NumberParseException:
        valid = False
    finally:
        if not valid:
            raise ValidationError("Phone number is not a valid UK number.")
