from rest_framework import serializers

from comment.models import Comment


class CommentsOfProductSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('user',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
