from rest_framework import serializers
from category.models import Category


class CategoryNestedSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['name', 'path']

    def get_path(self, obj):
        return str(obj)
