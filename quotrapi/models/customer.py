"""Customer model module"""
from django.db import models
from django.core.validators import validate_slug

class Customer(models.Model):
    """Customer database module"""
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    organization = models.CharField(max_length=75)
    email = models.EmailField(max_length=55,)