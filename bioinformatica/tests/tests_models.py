from django.test import TestCase
from bioinformatica.models import Client, Project, Experiment, Sample, FastQ, FastQFile


class ClientTestCase(TestCase):

    def setUp(self):
        self.client1 = client = Client.objects.create(
            name='Lucas',
            surname='Viatri',
            direction='18 de julio 1234',
            phone='099123465'
        )
        self.project1 = project = Project.objects.create(
            name='Proyecto1',
            contact=self.client1
        )
        self.experiment1 = experiment = Experiment.objects.create(
            name='Experimento1'
        )
        self.sample1 = sample = Sample.objects.create(
            experiment=experiment,
            responsible='Responsable1',
            location='Locacion1'
        )
        self.fastQ1 = fastQ = FastQ.objects.create(
            sample=sample,
            name='FastQ1'
        )
        # self.fastQFile = FastQFile = FastQFile.objects.create(
        #     fastQ=fastQ,
        #     file='QUE VA ACA?'
        # )

    def test_create_client(self):
        """A Client is created"""
        lucas = Client.objects.get(name='Lucas')
        self.assertEquals(lucas.name, 'Lucas')

    def test_create_project(self):
        """A Project is created"""
        proyecto = Project.objects.get(name='Proyecto1')
        self.assertEquals(proyecto.name, 'Proyecto1')

    def test_create_experiment(self):
        """An Experiment is created"""
        experimento = Experiment.objects.get(name='Experimento1')
        self.assertEquals(experimento.name, 'Experimento1')

    def test_create_sample(self):
        muestra = Sample.objects.get(experiment=self.experiment1)
        self.assertEquals(muestra.experiment, self.experiment1)

    def test_create_fastQ(self):
        fastq = FastQ.objects.get(name='FastQ1')
        self.assertEquals(fastq.name, 'FastQ1')

