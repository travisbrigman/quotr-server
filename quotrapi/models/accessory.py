"""Acessory model module"""
from django.db import models


class Accessory(models.Model):
    """Accessory database module"""
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="item" )
    accessory = models.ForeignKey("Accessory", on_delete=models.CASCADE, related_name="accessory" )