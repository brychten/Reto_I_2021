from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
               Clase que extiende el CustomUserCreationForm para agregarle el CI
               tanto al crear un usuario como al modificar uno ya creado
    """

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('CI',)





