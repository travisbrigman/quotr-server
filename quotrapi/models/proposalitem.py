"""ProposalItem model module"""
from django.db import models


class ProposalItem(models.Model):
    """ProposalItem database module"""
    proposal = models.ForeignKey("Proposal", on_delete=models.CASCADE, related_name="proposalitems" )
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="proposalitems" )
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="proposalItem_category", null=True )