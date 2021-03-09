from django.core.management.base import BaseCommand
import subprocess
import os


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command')
        parser.add_argument('name')
        parser.add_argument('project_id')
        parser.add_argument('--experiment_id')
        parser.add_argument('--location', default='Montevideo')

    def get_absolute_path(self, experiment_id, project_id, filter_var=False):
        path_list = []
        p = subprocess.Popen('pwd', shell=True, stdout=subprocess.PIPE)
        # p = subprocess.Popen('echo %cd%', shell=True, stdout=subprocess.PIPE)
        out = p.communicate()[0].decode("utf-8").rstrip('\r\n') + '\\media\\UploadedFiles\\PROJ_' + str(
            project_id) + '\\EXP_' + str(experiment_id) + '\\'
        out = out.replace('\\', '/')
        d = []
        for file in os.listdir(out.rstrip('\r\n')):
            r = os.path.join(out, file)
            d.append(r)
        for direccion in d:
            for base, dirs, files in os.walk(direccion):
                base = base.replace('\\', '/')
                if not filter_var:
                    path_list.append(base)
                else:
                    for file in files:
                        if file.__contains__('archivo_0.txt'):
                            path_list.append(base + '/' + file)
        return path_list

    def handle(self, *args, **options):
        # if options['command'] == 'agrupar':
        exp_id = options['experiment_id']
        project_id = options['project_id']
        print(options['command'].split('\r\n'))
        list_commands = options['command'].split('\r\n')
        for command in list_commands:
            if command.__contains__('cat'):
                path_list = self.get_absolute_path(exp_id, project_id)
                for base in path_list:
                    # command = 'for %a in (*.txt) do type “%a” >> archivo_0.txt'
                    command = 'awk 1 *.txt > archivo_0.txt'
                    if base.__contains__('FQ_'):
                        subprocess.Popen(command, shell=True, cwd=base)
            if command.__contains__('nextflow'):
                main_nf = os.environ.get("MAIN_NF")
                db_16s = os.environ.get("DB_16S")
                db_18s = os.environ.get("DB_18S")
                db_tax = os.environ.get("DB_TAX")

                list_path = self.get_absolute_path(exp_id,project_id,filter_var=True)

                for path in list_path:
                    path_sample = path.split('/FASTQs/')[0]
                    print("nextflow run %s -profile docker --reads %s  --db %s --tax %s mv results %s"
                          %(main_nf,path,db_16s,db_tax,path_sample))
