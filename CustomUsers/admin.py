from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    """
            Clase que extiende el UserAdmin, para de esta forma usar CustomUserCreationForms y poder
            asi crear CustomUsers
    """

    add_form = CustomUserCreationForm

    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('CI',)}),)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'CI')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),)


admin.site.register(CustomUser, CustomUserAdmin)




