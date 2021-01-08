"""View module for handling requests about items"""
import uuid, base64
from django.core.files.base import ContentFile
from quotrapi.models.item import Item
from quotrapi.models.accessory import Accessory
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class AccessorySerializer(serializers.ModelSerializer):
    """Accessory Serializer"""
    class Meta:
        model = Accessory
        fields = ('accessory',)
        depth = 1


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for items """

    # accessories = AccessorySerializer(many=True)

    class Meta:
        model = Item
        url = serializers.HyperlinkedIdentityField(
            view_name='item',
            lookup_field='id'
        )
        fields = ('id', 'make', 'model', 'cost', 'margin', 'description', 'image_path', 'created_on', 'sell_price')


class Items(ViewSet):
    """ items for quotr catalog"""

    def retrieve(self, request, pk=None):
        """gets single item from database"""

        try:
            item = Item.objects.get(pk=pk)

            serializer = ItemSerializer(item, context={'request': request})

            return Response(serializer.data)

        except Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """list all items"""
        cost = self.request.query_params.get('cost', None)
        make = self.request.query_params.get('make', None)

        items = Item.objects.all()

#TODO: This only filters fro a price greater than the number entered. Ideally, a min_price and max_price would be great
        if cost is not None:
            def price_filter(item):
                if item.cost >= float(cost):
                    return True
                return False

            items = filter(price_filter, items)

        if make is not None:
            items = items.filter(make__contains=make)


        serializer = ItemSerializer(
            items, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """creates new item in database"""

        new_item = Item()
        new_item.make = request.data["make"]
        new_item.model = request.data["model"]
        new_item.description = request.data["description"]
        new_item.margin = request.data["margin"]
        new_item.cost = request.data["cost"]
        new_item.created_on = request.data["created_on"]
        if "image_path" in request.data:
            format, imgstr = request.data["image_path"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{new_item.id}-{request.data["model"]}.{ext}')
            new_item.image_path = data

        new_item.save()

        serializer = ItemSerializer(
            new_item, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """updates single item in database"""

        item = Item.objects.get(pk=pk)
        item.make = request.data["make"]
        item.model = request.data["model"]
        item.description = request.data["description"]
        item.margin = request.data["margin"]
        item.cost = request.data["cost"]
        item.created_on = request.data["created_on"]
        if "image_path" in request.data:
            if request.data["image_path"] is not None:
                format, imgstr = request.data["image_path"].split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{item.id}-{request.data["model"]}.{ext}')
                item.image_path = data
        item.save()

        serializer = ItemSerializer(
            item, context={'request': request})

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        item = Item.objects.get(pk=pk)
        # item.make = request.data["make"]
        # item.model = request.data["model"]
        # item.description = request.data["description"]
        item.margin = request.data["margin"]
        # item.cost = request.data["cost"]
        # item.created_on = request.data["created_on"]
        # item.image_url = request.data["image_url"]
        item.save()

        serializer = ItemSerializer(item, context={'request': request}, partial=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)