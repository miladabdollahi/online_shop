from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.response import Response

from extended_lib.rest_framework import mixins
from extended_lib.rest_framework import permissions as perm
from comment.models import Comment
from comment.serializers import CommentsOfProductSerializer


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentsOfProductSerializer
    permission_classes = [perm.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        comment = Comment.objects.filter(user=request.user, product=request.data.get('product'))
        if comment.exists():
            return Response({
                'error': True,
                'data': {
                    'msg': _('this comment already exist!')
                }
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'error': False,
            'data': serializer.data,
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
