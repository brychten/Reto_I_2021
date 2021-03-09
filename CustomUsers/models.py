from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _



def civalidatator(value):
    """
               Se encarga de verificar si es un CI (tiene un largo de 8 caracteres y todos son numeros)
    """
    error_message = _("Invalid ID, there must not be characters like - or . only the ID number")
    if len(str(value)) == 8 and str(value).isnumeric():
        return value
    else:
        raise ValidationError(error_message)


class CustomUser(AbstractUser):
    """
               Clase que extiende el Usuario (no admin), permite extender la clase User base de django.
    """
    CI = models.CharField(max_length=8, blank=False, null=False, validators=[civalidatator])

    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )











