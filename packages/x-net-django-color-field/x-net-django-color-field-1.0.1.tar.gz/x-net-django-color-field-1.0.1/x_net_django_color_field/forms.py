from django.forms import (
    fields,
)

from x_net_django_color_field.validators import color_validator


################################################################################
# COLOR

class ColorField(fields.CharField):
    """Field to input and validate hex colors."""

    default_validators = [color_validator]
