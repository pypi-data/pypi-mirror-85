import re

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


################################################################################
# COLOR

COLOR_RE = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

color_validator = RegexValidator(
    COLOR_RE, _("Enter a valid color value: e.g. \"#FF0022\""), "invalid"
)
