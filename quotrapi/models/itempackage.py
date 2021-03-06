"""ItemPackage model module"""
from django.db import models


class ItemPackage(models.Model):
    """ItemPackagee database module"""
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="itemPackage_item" )
    package = models.ForeignKey("Package", on_delete=models.CASCADE, related_name="itemPackage_package" )