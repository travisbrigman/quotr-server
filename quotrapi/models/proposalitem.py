"""ProposalItem model module"""
from django.db import models


class ProposalItem(models.Model):
    """ProposalItem database module"""
    proposal = models.ForeignKey("Proposal", on_delete=models.CASCADE, related_name="proposal" )
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="item" )
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category" )