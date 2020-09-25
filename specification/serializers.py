from rest_framework import serializers

from specification.models import Specification


class RecursiveField(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class SpecificationSerializer(serializers.ModelSerializer):
    childs = RecursiveField(many=True)
    path = serializers.SerializerMethodField()

    class Meta:
        model = Specification
        fields = '__all__'

    def get_path(self, obj):
        return str(obj)
