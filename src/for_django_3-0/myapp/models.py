from django.db import models

from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
from django.utils import timezone

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    time_stamp =models.DateTimeField(default=timezone.now)
    doctype = models.CharField(max_length=50, default='Not_Defined')

    def delete(self, *args, **kwargs):
        # first, delete the file
        self.docfile.delete(save=False)

        # now, delete the object
        super(Document, self).delete(*args, **kwargs)

