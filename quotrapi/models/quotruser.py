"""Database QuotrUser module"""
from django.db import models
from django.contrib.auth.models import User


class QuotrUser(models.Model):
    """QuotrUser database model"""
    profile_image = models.ImageField(
        upload_to='quotrusers', height_field=None,
        width_field=None, max_length=None, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    @property
    def is_current_user(self):
        return self.__is_current_user

    @is_current_user.setter
    def is_current_user(self,value):
        self.__is_current_user = value
