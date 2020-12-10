"""ProposalItem model module"""
from django.db import models


class ProposalItem(models.Model):
    """ProposalItem database module"""
    proposal = models.ForeignKey("Proposal", on_delete=models.CASCADE, related_name="proposItem_proposal" )
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="proposalItem_item" )
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="proposalItem_category" )