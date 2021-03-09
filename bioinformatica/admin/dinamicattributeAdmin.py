from django.contrib import admin
from bioinformatica.models.dinamicattribute import DynamicAttributeDefinition
from bioinformatica.models.dinamicattribute import DynamicAttributeInstance
from bioinformatica.models.logicaldelete import LogicalDeletedModelAdmin, LogicaLDeletedModelTabularInLine
from admin_confirm.admin import confirm_action, AdminConfirmMixin


class AttributeInline(LogicaLDeletedModelTabularInLine):
    model = DynamicAttributeInstance
    extra = 1
    fields = ['attribute_type', 'attribute_value']


class DynamicAttributeDefinitionAdmin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    list_display = ('attribute_name', 'attribute_description')
    search_fields = ['attribute_name']

    confirm_change = True
    confirm_add = True
    confirmation_fields = ['attribute_name', 'attribute_description']


class DynamicAttributeInstanceAdmin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    fieldsets = [
        (None, {'fields': ['attribute_type']}),
        ('Value', {'fields': ['attribute_value']}),
    ]

    confirm_change = True
    confirm_add = True
    confirmation_fields = ['attribute_name', 'attribute_value']


admin.site.register(DynamicAttributeDefinition, DynamicAttributeDefinitionAdmin)
admin.site.register(DynamicAttributeInstance, DynamicAttributeInstanceAdmin)
