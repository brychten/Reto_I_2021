from django.db import models
from django.utils import timezone
from .logicaldelete import LogicalDeletedModel
from django.utils.translation import gettext as _
import logging

logger = logging.getLogger(__name__)


class Experiment(LogicalDeletedModel):
    experiment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    place = models.CharField(max_length=200)
    date = models.DateTimeField(_('Date'), default=timezone.now)
    location = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=120)
    project_id = models.ForeignKey('Project', on_delete=models.DO_NOTHING, blank=True, null=True)
    executionCommands = models.TextField(blank=True)

    def __str__(self):
        return self.name
