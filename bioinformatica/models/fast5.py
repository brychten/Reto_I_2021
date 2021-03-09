from django.db import models
from .logicaldelete import LogicalDeletedModel
from django.utils.translation import gettext as _
from RetoI.settings import UPLOAD_ROOT
import os


def get_upload_path(instance, filename):
    fast5_head = instance.fast5.fast5_id
    sample_head = instance.fast5.sample.sample_id
    experiment_head = instance.fast5.sample.experiment.experiment_id
    project_head = instance.fast5.sample.experiment.project_id.project_id
    return os.path.join("%s/PROJ_%s/EXP_%s/SAMP_%s/FAST5s/F5_%s/%s" %
                        (UPLOAD_ROOT, project_head, experiment_head, sample_head, fast5_head, filename))


class Fast5(LogicalDeletedModel):
    fast5_id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=240)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True, editable=True)
    file = models.FileField(upload_to=get_upload_path, verbose_name="Load fast5 File",
                            help_text='Seleccione El archivo Fast5', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Fast5, self).save(*args, **kwargs)
        filename = self.file.url
        print(self.file)
