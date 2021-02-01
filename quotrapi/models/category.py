"""Category model module"""
from django.db import models


class Category(models.Model):
    """Category database module"""
    
    label = models.CharField(max_length=55)