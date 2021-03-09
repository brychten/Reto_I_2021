from django.contrib import admin
from bioinformatica.models.fast5 import Fast5
from bioinformatica.models.logicaldelete import LogicalDeletedModelAdmin, LogicaLDeletedModelTabularInLine
from admin_confirm.admin import confirm_action, AdminConfirmMixin


class Fast5Inline(LogicaLDeletedModelTabularInLine):
    model = Fast5
    extra = 0
    classes = ['collapse']


class Fast5Admin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    search_fields = ['date_created']

    confirm_change = True
    confirm_add = True
    confirmation_fields = ['date_created', 'file']


class Fast5FileAdmin(LogicalDeletedModelAdmin):
    pass


admin.site.register(Fast5, Fast5Admin)
