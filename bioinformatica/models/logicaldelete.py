"""Administration of logical deleted models."""
import itertools
from django.contrib import admin
from django.forms import ModelForm
from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db import DEFAULT_DB_ALIAS
from django.contrib.admin.utils import NestedObjects


class LogicalDeletedManager(models.Manager):
    """A base class for entity managers that support logical deletes. A logical
    delete does not remove the entity records from the DB, but marks the record
    as deleted using a record field."""
    def get_queryset(self):
        """Returns a query set of instances not deleted from the DB"""
        return super(LogicalDeletedManager, self).get_queryset().filter(removed__isnull=True)

    def everything(self):
        """Returns a query set with all the instances of the DB, including
        deleted instances."""
        if self.model:
            return super(LogicalDeletedManager, self).get_queryset()

    def only_deleted(self):
        """Returns a query set with all the deleted instances of the DB"""
        if self.model:
            return super(LogicalDeletedManager, self).get_queryset().filter(removed__isnull=False)

    def get(self, *args, **kwargs):
        """Gets an object, the search will be performed including deleted
        entities."""
        return self.everything().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        """Gets a queryset, the search will be performed including deleted
        entities."""
        if 'pk' in kwargs:
            return self.everything().filter(*args, **kwargs)
        return self.get_queryset().filter(*args, **kwargs)


class LogicalDeletedModel(models.Model):
    """A base class for entities that support logical deletes. A logical
    delete does not remove the entity records from the DB, but marks the record
    by using the 'removed' field."""
    created = models.DateTimeField(default=timezone.now)
    removed = models.DateTimeField(null=True, blank=True , db_index=True)

    objects = LogicalDeletedManager()

    def active(self):
        """Returns True if the entity has not been removed from the DB."""
        return self.removed == None
    active.boolean = True

    # def delete(self):
    #     """Logical deletes the entity from the DB, setting it's 'removed' field
    #     to the current time."""
    #     self.removed = timezone.now()
    #     self.save()

    def delete(self):
        # Fetch related models
        to_delete = get_related_objects(self)

        for obj in to_delete:
            obj.delete()

        # Soft delete the object
        self.removed = timezone.now()
        self.save()

    class Meta:
        """Meta class for Django."""
        abstract = True


class LogicaLDeletedModelTabularInLine(admin.TabularInline):
    exclude = ('created', 'modified', 'removed')

    def get_queryset(self, request):
        """Overriden to return all the objects, even the logical deleted ones."""
        qs = self.model._default_manager.get_queryset()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class LogicalDeletedModelAdmin(admin.ModelAdmin):
    """Base clase for models which support logical deletes."""
    list_display = ('__str__', )
    list_display_filter = ('active',)
    exclude = ('created', 'modified', 'removed', )

    actions = ['delete_model',]

    def get_actions(self, request):
        actions = super(LogicalDeletedModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        if (isinstance(obj, LogicalDeletedModel)):
            obj.delete()
        else:
            for o in obj:
                o.delete()

    delete_model.short_description = _("Delete selected items")

    def get_queryset(self, request):
        """Overriden to return all the objects, even the logical deleted ones."""
        qs = self.model._default_manager.get_queryset()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

class LogicalDeletedMeta:
    """Django admin meta for logical delete models."""
    exclude = ('created', 'modified', 'removed')

class LogicalDeletedForm(ModelForm):
    """Base form for logical deleted model administration."""
    class Meta(LogicalDeletedMeta):
        """Use LogicalDeletedMeta by default."""
        pass

# Aux to get nested objects (relationships, etc)
def get_related_objects(obj, using=DEFAULT_DB_ALIAS):
    collector = NestedObjects(using=using)
    collector.collect([obj])

    def flatten(elem):
        if isinstance(elem, list):
            return itertools.chain.from_iterable(map(flatten, elem))
        elif obj != elem:
            return (elem,)
        return ()

    return flatten(collector.nested())