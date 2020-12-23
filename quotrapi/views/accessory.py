"""View module for handling requests about Accessories"""
from quotrapi.models.item import Item
from quotrapi.models.accessory import Accessory
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class AccessorySerializer(serializers.ModelSerializer):
    """JSON serializer for Accessories"""
    class Meta:
        model = Accessory
        fields = ('item_id', 'accessory_id')

class Accessories(ViewSet):
    """accessories of items"""

    def create(self, request):
        """creates a new accessory relationship"""
        try:
            item = Item.objects.get(id=request.data["item_id"])
        except Item.DoesNotExist:
            return Response({'message: invalid item id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            accessory = Item.objects.get(id=request.data["accessory_id"])
        except Item.DoesNotExist:
            return Response({'message: invalid accessory id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        new_accessory = Accessory()
        new_accessory.item = item
        new_accessory.accessory = accessory

        try:
            new_accessory.save()
            serializer = AccessorySerializer(new_accessory, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
