from django.db import models
from bioinformatica.models.experiment import Experiment
from .logicaldelete import LogicalDeletedModel


class DynamicAttributeDefinition(LogicalDeletedModel):
    """Clase que modela la definicion de Attributo, es decir, la que define el nombre del attributo, no el valor"""
    dynamicAttributeDef_id = models.AutoField(primary_key=True)
    attribute_name = models.CharField(max_length=120)
    attribute_description = models.TextField(max_length=120, blank=True)

    def __str__(self):
        return self.attribute_name


class DynamicAttributeInstance(LogicalDeletedModel):
    """
            Clase que modela cada instancia especifica de Attributo, es decir, la que define el valor, y no el nombre del
            attributo, para el tipo de atributo, es decir, para su nombre, esta clase tiene una relacion ManyToOne con
            DynamicAttributeDefinition
    """
    dynamicAttributeInst_id = models.AutoField(primary_key=True)
    experiment_attributes = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    attribute_type = models.ForeignKey(
        DynamicAttributeDefinition,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
    attribute_value = models.CharField(max_length=120)

    def __str__(self):
        return str(self.attribute_type)
