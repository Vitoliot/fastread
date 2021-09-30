from django.core.exceptions import ValidationError
from django.core.validators import validate_integer

def procent_validator(data):
    validate_integer(data)
    if (data > 100) or (data < 0): raise ValidationError
    return data