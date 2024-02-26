from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[a-zA-Z_][a-zA-Z0-9_]{0,49}$"
    message = _(
        "Enter a valid username. Username may contain only letters, "
        "numbers and underscores."
    )
    flags = 0
