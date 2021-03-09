from django.contrib import admin
from bioinformatica.models.project import Project
from bioinformatica.models.logicaldelete import LogicalDeletedModelAdmin, LogicaLDeletedModelTabularInLine
from bioinformatica.admin.experimentAdmin import ExperimentInline
from admin_confirm.admin import AdminConfirmMixin


class ProjectAdmin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    list_display = ('name', 'contact', 'create_date')
    list_filter = ['create_date']
    search_fields = ['name', 'contact__name', 'contact__lastname']
    inlines = [ExperimentInline]
    fieldsets = [
        (None, {'fields': [('name', 'contact')]}),
        ('Project information', {'fields': ['create_date', 'description'], 'classes':['collapse']}),
    ]

    #confirm_change = True
    confirm_add = True
    confirmation_fields = ['name', 'description', 'contact']


admin.site.register(Project, ProjectAdmin)
