from django.db import models
from .logicaldelete import LogicalDeletedModel
from django.utils.translation import gettext as _

from RetoI.settings import UPLOAD_ROOT


class Sample(LogicalDeletedModel):
    sample_id = models.AutoField(primary_key=True)
    experiment = models.ForeignKey(_('Experiment'), on_delete=models.CASCADE)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True, editable=True)
    responsible = models.CharField(_('Responsible'), max_length=120)
    location = models.CharField(_('Location'), max_length=120)

    def __str__(self):
        return '%s-%s' %(self.experiment.name, self.sample_id)

    def get_path_fastQ_file(self):
        return ("%s/PROJ_%s/EXP_%s/SAMP_%s/FASTQs/" %
                (UPLOAD_ROOT, self.experiment.project_id.project_id, self.experiment.experiment_id, self.sample_id))

    def get_sample_id(self):
        return self.sample_id

    def get_experiment_id(self):
        return self.experiment.experiment_id


