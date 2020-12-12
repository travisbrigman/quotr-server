"""View module for handling requests about customers"""
from quotrapi.models.customer import Customer
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers"""
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'email', 'first_name', 'last_name', 'organization')


class Customers(ViewSet):
    """customers for quotr proposals"""

    def retrieve(self, request, pk=None):
        """gets single customer from database"""

        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})

            return Response(serializer.data)

        except Customer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """list all customers"""
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True, context={'request': request})

        return Response(serializer.data)
