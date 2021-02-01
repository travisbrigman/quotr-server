"""Quotr User Views Module"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from quotrapi.models import QuotrUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'date_joined', 'is_staff', 'is_active')

class QuotrUserSerializer(serializers.ModelSerializer):
    """Serializer for QuotrUser Info"""
    user = UserSerializer(many=False)

    class Meta:
        model = QuotrUser
        fields = ('id', 'user', 'is_current_user', 'profile_image')

class QuotrUsers(ViewSet):
    """QuotrUser Class"""

    def list(self, request):
        """ handles GET all"""
        users = QuotrUser.objects.all()

        serializer = QuotrUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
    
        try:
            user = QuotrUser.objects.get(pk=pk)
            
            #logic to set an unmapped property on QuotrUser 
            #will let front end determine if the user retrieved by this function is the current user
            if request.auth.user.id == int(pk):
                user.is_current_user = True
            else:
                user.is_current_user = False

            serializer = QuotrUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def partial_update(self, request, pk=None):
        quotr_user = QuotrUser.objects.get(pk=pk)
        quotr_user.profile_image = request.data["profile_image"]
        quotr_user.save()

        serializer = QuotrUserSerializer(quotr_user, context={'request': request}, partial=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    


