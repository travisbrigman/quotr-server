from django.db import models
from .customer import Customer
from django.contrib.auth.models import User


class Proposal(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name='proposals')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='proposals')
    export_date = models.DateTimeField(null=True)