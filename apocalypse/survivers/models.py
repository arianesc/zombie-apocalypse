from django.db import models
from django.core.validators import MinValueValidator


class Surviver(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    gender = models.CharField( max_length=10)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    food = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    water = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    medication = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    ammunition = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    infected = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self.name