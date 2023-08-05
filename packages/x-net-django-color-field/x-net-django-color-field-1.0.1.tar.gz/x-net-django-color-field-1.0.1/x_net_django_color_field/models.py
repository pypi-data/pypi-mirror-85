from django.db import models

from x_net_django_color_field.validators import color_validator


################################################################################
# COLOR

class ColorField(models.CharField):
    default_validators = [color_validator]

    def __init__(self, *args, **kwargs):
        """Field to input and validate hex colors."""
        kwargs.setdefault("max_length", 7)
        super().__init__(*args, **kwargs)
