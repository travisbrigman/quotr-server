from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Item(models.Model):

    make = models.CharField(max_length=55)
    model = models.CharField(max_length=75)
    cost = models.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(25_500.00)],)
    margin = models.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(1.99)],)
    description = models.CharField(max_length=300)
    image_url = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
