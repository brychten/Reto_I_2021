from django.contrib import admin
from bioinformatica.models.sample import Sample
from bioinformatica.models.logicaldelete import LogicaLDeletedModelTabularInLine, LogicalDeletedModelAdmin
from bioinformatica.admin.fastQAdmin import FastQInline
from admin_confirm.admin import confirm_action, AdminConfirmMixin


class SampleAdmin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    search_fields = ['experiment__name', 'date_created', 'location']
    list_display = ('sample_id', 'experiment', 'responsible', 'location')
    inlines = [FastQInline]

    confirm_change = True
    confirm_add = True
    confirmation_fields = ['experiment', 'date_created', 'responsible', 'location']


class SamplesInline(LogicaLDeletedModelTabularInLine):
    model = Sample
    extra = 0


admin.site.register(Sample, SampleAdmin)
