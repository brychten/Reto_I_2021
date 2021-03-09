import os

from django.core.files.storage import FileSystemStorage
from django.db import models
from .logicaldelete import LogicalDeletedModel
from RetoI.settings import UPLOAD_ROOT
from django.utils.translation import gettext as _


class FastQ(LogicalDeletedModel):
    fastQ_id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=240)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True, editable=True)

    def __str__(self):
        return self.name


class UploadRootStorage(FileSystemStorage):
    def __init__(self):
        """Create the storage."""
        FileSystemStorage.__init__(self,
                                   location=UPLOAD_ROOT,
                                   base_url='/'
                                   )


def get_upload_path(instance, filename):
    fastQ_head = instance.fastQ.fastQ_id
    sample_head = instance.fastQ.sample.sample_id
    experiment_head = instance.fastQ.sample.experiment.experiment_id
    project_head = instance.fastQ.sample.experiment.project_id.project_id
    return os.path.join("%s/PROJ_%s/EXP_%s/SAMP_%s/FASTQs/FQ_%s/%s" %
                        (UPLOAD_ROOT, project_head, experiment_head, sample_head, fastQ_head, filename))


class FastQFile(LogicalDeletedModel):
    fastQ = models.ForeignKey(FastQ, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to=get_upload_path, verbose_name="Load fastQ File",
                            help_text='Seleccione El archivo FastQ')

    def __str__(self):
        return self.fastQ.name

    def save(self, *args, **kwargs):
        super(FastQFile, self).save(*args, **kwargs)
        filename = self.file.url
        print(self.file)
