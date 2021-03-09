from django.core.management.base import BaseCommand, CommandError
from bioinformatica.models import Experiment as Experiment

class Command(BaseCommand):
    help ='The help information for this command'

    def add_arguments(self, parser):
        parser.add_argument('first',type=int,help ='A number less than 100')
        parser.add_argument('second',nargs=3,type=str,help='Three strings')
        parser.add_argument('--option1',default='default',help='The option1 value')
        parser.add_argument('--option2',action='store_true',help='True if passed')

    #    parser.add_argument('experiment_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        #print('My command')
        #print(f'First: {options["first"]}')
        #print(f'Option1: {options["option1"]}')
        #self.stdout.write(self.style.SUCCESS('Successfully closed experiment "%s"' % experiment_id))

        if options['first'] < 100:
            self.stdout.write(self.style.SUCCESS('Good job. The number is less than 100'))
        else:
            raise CommandError('That number is greater than 100.')
        for value in options['second']:
            self.stdout.write(f'Value: {value}')
        self.stdout.write(f'The value of --option1 is {options["option1"]}')
        if options['option2']:
            self.stdout.write(self.style.SUCCESS('Option 2 is TRUE'))
        else:
            self.stdout.write(self.style.WARNING('Option 2 is FALSE'))