from rest_framework import validators
from django.utils.translation import gettext_lazy as _


class UniqueValidator(validators.UniqueValidator):
    message = {
        'msg': _('This field must be unique.')
    }

    def include_current_instance(self, instance, serializer_field, value):
        for field in serializer_field.source_attrs:
            instance = getattr(instance, field)
        return bool(instance == value)

    def __call__(self, value, serializer_field):
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        field_name = serializer_field.source_attrs[-1]
        # Determine the existing instance, if this is an update operation.
        instance = getattr(serializer_field.parent, 'instance', None)

        queryset = self.queryset
        queryset = self.filter_queryset(value, queryset, field_name)
        if validators.qs_exists(queryset) and not self.include_current_instance(instance, serializer_field, value):
            raise validators.ValidationError(self.message, code='unique')
