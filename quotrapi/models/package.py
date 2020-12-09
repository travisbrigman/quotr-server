"""Package model module"""
from django.db import models


class Package(models.Model):
    """Package database module"""
    
    label = models.CharField(max_length=55)