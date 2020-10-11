from rest_framework import serializers

from category.models import Category


class CategoryNestedSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['name', 'path']

    def get_path(self, obj):
        return str(obj)


class RecursiveField(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

    class Meta:
        model = Category
        fields = ('id', 'name', 'childs', 'specification')


class CategorySerializer(serializers.ModelSerializer):
    childs = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'childs', 'specification')


class CategroyParentSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'specification')

    def get_parent(self, obj):
        if obj.parent is not None:
            return CategroyParentSerializer(obj.parent).data
        else:
            return None