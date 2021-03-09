from celery import shared_task
from django.core.management import call_command


@shared_task
def experiment_commands(experiment_info):
    call_command("experimentCommand", experiment_info[0], experiment_info[1], experiment_info[2],
                 experiment_id=experiment_info[3])

