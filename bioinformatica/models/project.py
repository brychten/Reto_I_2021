from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _
from .logicaldelete import LogicalDeletedModel


class Project(LogicalDeletedModel):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    create_date = models.DateTimeField(_('Create date'), default=datetime.now(), editable=True)
    contact = models.ForeignKey('Contact', on_delete=models.DO_NOTHING, null=False, blank=False)

    def __str__(self):
        return self.name
