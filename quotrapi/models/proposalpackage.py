"""ProposalPackage model module"""
from django.db import models


class ProposalPackage(models.Model):
    """ProposalPackage database module"""
    package = models.ForeignKey("Package", on_delete=models.CASCADE, related_name="package" )
    proposal = models.ForeignKey("Proposal", on_delete=models.CASCADE, related_name="proposal" )
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category" )