from django.contrib import admin
from bioinformatica.models.client import Client, Contact
from bioinformatica.models.logicaldelete import LogicalDeletedModelAdmin, LogicaLDeletedModelTabularInLine
from admin_confirm.admin import confirm_action, AdminConfirmMixin


class ClientInline(LogicaLDeletedModelTabularInLine):
    model = Client
    extra = 0
    classes = ['collapse']


class ContactInLine(LogicaLDeletedModelTabularInLine):
    model = Contact
    extra = 0
    classes = ['collapse']


class ClientAdmin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    list_display = ['name', 'address', 'phone', ]
    search_fields = ['name']
    inlines = [ContactInLine]
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Client Data', {'fields': ['address', ('phone', 'email')], 'classes': ['collapse']}),
    ]

    confirm_change = True
    confirm_add = True
    confirmation_fields = ['name', 'address', 'phone', 'email']


class ContactAdmin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    list_display = ('name', 'last_name', 'phone', 'client')
    search_fields = ['name', 'last_name', 'client__name']

    confirm_change = True
    confirm_add = True
    confirmation_fields = ['name', 'last_name', 'client', 'phone', 'email']


admin.site.register(Client, ClientAdmin)
admin.site.register(Contact, ContactAdmin)

