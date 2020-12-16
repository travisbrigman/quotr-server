"""Proposal model module"""
from quotrapi.models.quotruser import QuotrUser
from django.db import models
from .customer import Customer
from django.contrib.auth.models import User


class Proposal(models.Model):
    """Proposal database module"""
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name='proposals', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(QuotrUser, on_delete=models.DO_NOTHING, related_name='proposals')
    export_date = models.DateTimeField(null=True)