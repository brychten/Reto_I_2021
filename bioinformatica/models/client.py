from django.db import models
from django.utils.translation import gettext as _
from .logicaldelete import LogicalDeletedModel


class Client(LogicalDeletedModel):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(_('Client name'), max_length=200)
    address = models.CharField(_('Address'), max_length=200)
    email = models.CharField('E-mail', max_length=200, blank=True)
    phone = models.CharField(_('Phone'), max_length=200)

    def __str__(self):
        return self.name


class Contact(LogicalDeletedModel):
    contact_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(_('Name'), max_length=200)
    last_name = models.CharField(_('Last name'), max_length=200)
    email = models.CharField('E-mail', max_length=200, blank=True)
    phone = models.CharField(_('Phone'), max_length=200)

    def __str__(self):
        return '%s (%s)' % (self.name, self.client)
