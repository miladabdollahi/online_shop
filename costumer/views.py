from rest_framework import viewsets
from rest_framework.response import Response

from costumer.models import Costumer
from costumer.serializers import CostumerSerializer
from extended_lib.rest_framework import permissions as perm
from extended_lib.rest_framework import mixins


class CostumerViewSet(viewsets.GenericViewSet,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin):
    queryset = Costumer.objects.all()
    serializer_class = CostumerSerializer
    permission_classes = [perm.IsAuthenticated, perm.IsOwner]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'error': False,
            'data': serializer.data
        })
