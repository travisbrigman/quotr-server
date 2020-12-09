from django.db import models
from django.core.validators import validate_email, validate_slug

class Customer(models.Model):
    first_name = models.CharField(max_length=55, validators=validate_slug)
    last_name = models.CharField(max_length=55, validators=validate_slug)
    organization = models.CharField(max_length=75, validators=validate_slug)
    email = models.CharField(max_length=55, validators=validate_email)