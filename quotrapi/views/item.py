"""View module for handling requests about items"""
from quotrapi.models.item import Item
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for items """
    class Meta:
        model = Item
        url = serializers.HyperlinkedIdentityField(
            view_name='item',
            lookup_field='id'
        )
        fields = ('id', 'make', 'model', 'cost', 'margin', 'description', 'image_url', 'created_on')


class Items(ViewSet):
    """Line items for Bangazon orders"""

    def retrieve(self, request, pk=None):

            try:
                item = Item.objects.get(pk=pk)

                serializer = ItemSerializer(item, context={'request': request})

                return Response(serializer.data)

            except Item.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)