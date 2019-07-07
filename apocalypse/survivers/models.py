from django.db import models
from django.core.validators import MinValueValidator


class Surviver(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    age = models.IntegerField(validators=[MinValueValidator(1)])
    gender = models.CharField( max_length=10)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
# Create your models here.
