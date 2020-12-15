"""View module for proposalitems"""
from django.contrib.auth.models import User
from quotrapi.models.quotruser import QuotrUser
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quotrapi.models import proposal
from quotrapi.models.proposal import Proposal
from quotrapi.models.item import Item
from quotrapi.models.proposalitem import ProposalItem


class ProposalItemSerializer(serializers.ModelSerializer):
    """JSON serializer for proposalitems"""
    class Meta:
        model = ProposalItem
        fields = ('id', 'proposal_id', 'item_id', 'category_id')
        

class ProposalItems(ViewSet):
    """proposalitems for quotr proposals"""

    

    def list(self, request):
        """
        lists all proposalitems
        """
        proposalitems = ProposalItem.objects.all()

        serializer = ProposalItemSerializer(
            proposalitems, many=True, context={'request' : request}
        )
        return Response(serializer.data)

    def create(self, request):
        """
        create a proposalitem object
        """
        current_user = User.objects.get(username=request.auth.user)
        try:
            item = Item.objects.get(id=request.data["item_id"])
        except Item.DoesNotExist:
            return Response({'message: invalid item id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            proposal = Proposal.objects.get(created_by=current_user.id, created_on__isnull=True)
        except Proposal.DoesNotExist:
            proposal = Proposal()
            proposal.customer = None
            proposal.created_by = current_user
            proposal.export_date = None
            proposal.save()

        proposalitem = ProposalItem()
        proposalitem.proposal = proposal
        proposalitem.item = item
        proposalitem.category = None

        try:
            proposalitem.save()
            serializer = ProposalItemSerializer(proposalitem, many=False, )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ DELETE """
        try:
            proposalitem = ProposalItem.objects.get(pk=pk)
            proposalitem.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except ProposalItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)