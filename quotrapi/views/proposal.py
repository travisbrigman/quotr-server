"""View module for handling requests about proposals"""
from quotrapi.models.item import Item
from quotrapi.views.proposalitem import ProposalItems
from quotrapi.models import customer
from quotrapi.models.customer import Customer
from quotrapi.models import proposal
from quotrapi.models.quotruser import QuotrUser
from django.conf.urls import url
from django.contrib.auth.models import User
from quotrapi.models.proposal import Proposal
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
import datetime
from quotrapi.models.proposalitem import ProposalItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """basic user serializer"""
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        fields = ('id',)

        # custom property, book 2 ch. 12

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    """Item Serializer"""
    class Meta:
        model = Item
        url = serializers.HyperlinkedIdentityField(
            view_name='item',
            lookup_field='id'
        )
        fields = ('id', 'make', 'model', 'cost', 'description', 'margin')
class ProposalItemSerializer(serializers.ModelSerializer):
    """Proposal Item Serializer"""
    class Meta:
        model = ProposalItem
    
        fields = ('item',)
        depth = 1


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """customer object serializer"""
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'first_name', 'last_name', 'email', 'organization')


class ProposalSerializer(serializers.ModelSerializer):
    """JSON serializer for proposals"""
    customer = CustomerSerializer(many=False)
    items = ProposalItemSerializer(many=True)

    class Meta:
        model = Proposal
        fields = ('id', 'created_on',
                  'created_by_user', 'export_date', 'customer', 'items')
        depth = 1


class Proposals(ViewSet):
    """proposals for quotr proposal view"""

    def retrieve(self, request, pk=None):
        """gets single proposal from database"""

        try:
            proposal = Proposal.objects.get(pk=pk)
            customer = Customer.objects.get(pk=proposal.customer_id)
            proposal.customer = customer

            serializer = ProposalSerializer(
                proposal, context={'request': request})

            return Response(serializer.data)

        except Proposal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """list all proposals"""
        proposals = Proposal.objects.all()

        serializer = ProposalSerializer(
            proposals, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):
        """creates a new proposal in the database"""

        current_user = QuotrUser.objects.get(user=request.auth.user)

        try:
            new_proposal = Proposal.objects.get(
                customer_id=request.data["customer_id"], export_date__isnull=True)
        except Proposal.DoesNotExist:
            customer = Customer.objects.get(pk=request.data["customer_id"])
            new_proposal = Proposal()
            new_proposal.customer = customer
            new_proposal.created_on = datetime.datetime.now()
            new_proposal.created_by = current_user
            new_proposal.export_date = None
            new_proposal.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """updates single proposal in database"""

        customer = Customer.objects.get(pk=request.data["customer_id"])
        proposal = Proposal.objects.get(pk=pk)
        proposal.customer = customer
        proposal.created_on = datetime.datetime.now()
        proposal.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            proposal = Proposal.objects.get(pk=pk)
            proposal.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Proposal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
