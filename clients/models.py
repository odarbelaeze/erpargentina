# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class Route(models.Model):

    name = models.CharField(max_length = 100)
    description = models.TextField()
    in_charge = models.OneToOneField(User)

    class Meta:
        ordering = ['name']
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"

    def __unicode__(self):
        return self.name
    
    