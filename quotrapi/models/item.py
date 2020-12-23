"""Item model module"""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Item(models.Model):
    """Item database module"""
    make = models.CharField(max_length=55)
    model = models.CharField(max_length=75)
    cost = models.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(25_500.00)],)
    margin = models.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(1.99)],)
    description = models.CharField(max_length=300)
    image_url = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def sell_price(self):
        """docstring"""
        if self.margin > 1:
            margin_percentage = self.margin / 100
        else:
            margin_percentage = self.margin

        margin_remainder = 1 - margin_percentage
        return round(self.cost / margin_remainder, 2)

