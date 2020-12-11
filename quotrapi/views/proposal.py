"""View module for handling requests about proposals"""
from django.conf.urls import url
from django.contrib.auth.models import User
from quotrapi.models.proposal import Proposal
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """basic user serializer"""
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        fields = ('id',)

class ProposalSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for proposals"""
    created_by = UserSerializer(many=False)
    class Meta:
        model = Proposal
        url = serializers.HyperlinkedIdentityField(
            view_name='proposal',
            lookup_field='id'
        )
        fields = ('id', 'customer_id', 'created_on', 'created_by', 'export_date')


class Proposals(ViewSet):
    """proposals for quotr proposal view"""

    def retrieve(self, request, pk=None):
        """gets single proposal from database"""

        try:
            proposal = Proposal.objects.get(pk=pk)

            serializer = ProposalSerializer(proposal, context={'request': request})

            return Response(serializer.data)

        except Proposal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
