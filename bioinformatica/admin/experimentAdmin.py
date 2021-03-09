from admin_confirm.admin import AdminConfirmMixin
from django.contrib import admin, messages
from bioinformatica.models.experiment import Experiment
from bioinformatica.admin.dinamicattributeAdmin import AttributeInline
from bioinformatica.admin.sampleAdmin import SamplesInline
from bioinformatica.models.logicaldelete import LogicalDeletedModelAdmin, LogicaLDeletedModelTabularInLine
import redis_lock
from bioinformatica.admin.tasks import experiment_commands


class ExperimentAdmin(AdminConfirmMixin, LogicalDeletedModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'executionCommands']}),
        ('Project id', {'fields': ['project_id']})
    ]

    confirm_change = True
    confirm_add = True
    confirmation_fields = ['name', 'project_id']

    actions = ["experiment_actions"]

    def experiment_actions(self, obj, queryset=[]):
        experiment_info = []
        for q in queryset:
            conn = redis_lock.StrictRedis(host='67.205.171.138', port=6379)
            lock = redis_lock.Lock(conn, "experimento" + str(q.pk))
            if lock.acquire(timeout=1):

                experiment_info.append(q.executionCommands)
                experiment_info.append(q.name)
                experiment_info.append(q.project_id.project_id)
                experiment_info.append(q.experiment_id)

                print(f"Tomando experimento nro: {q.pk}")

                experiment_commands.delay(experiment_info)

                lock.release()
            else:
                messages.add_message(obj, messages.INFO, 'Alguien ya está trabajando con este experimento')

    experiment_actions.short_description = 'RUN'
    experiment_actions.allow_tags = True
    list_display = ('name', 'location', 'state', 'project_id', 'experiment_actions')
    inlines = [SamplesInline, AttributeInline]
    list_filter = ['date']
    search_fields = ['name']


admin.site.register(Experiment, ExperimentAdmin)


class ExperimentInline(LogicaLDeletedModelTabularInLine):
    model = Experiment
    extra = 0
    classes = ['collapse']
