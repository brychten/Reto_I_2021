from django.contrib import admin
from bioinformatica.models.fastQ import FastQ, FastQFile
from bioinformatica.models.logicaldelete import LogicalDeletedModelAdmin, LogicaLDeletedModelTabularInLine
from admin_confirm.admin import confirm_action, AdminConfirmMixin


class FastQFileAdmin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    list_display = ('fastQ', 'file')

    confirm_change = True
    confirm_add = True
    confirmation_fields = ['fastQ', 'file']


class FastQFileInline(LogicaLDeletedModelTabularInLine):
    model = FastQFile
    extra = 0
    classes = ['collapse']


class FastQInline(LogicaLDeletedModelTabularInLine):
    model = FastQ
    extra = 0
    classes = ['collapse']


class FastQAdmin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    search_fields = ['date_created']
    inlines = [FastQFileInline]
    list_display = ('fastQ_id', 'name', 'sample')

    confirm_change = True
    confirm_add = True
    confirmation_fields = ['fastQ_id', 'name', 'sample']


admin.site.register(FastQ, FastQAdmin)
admin.site.register(FastQFile, FastQFileAdmin)
