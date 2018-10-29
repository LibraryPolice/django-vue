# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Book(models.Model):
    index_name = models.CharField(max_length=64)
    index_set = models.QuerySet
    def __unicode__(self):
        return self.index_name