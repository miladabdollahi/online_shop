from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from collections import OrderedDict


class ModelSerializer(serializers.ModelSerializer):
    def run_validation(self, data=serializers.empty):
        """
        We override the default `run_validation`, because the validation
        performed by validators and the `.validate()` method should
        be coerced into an error dictionary with a 'non_fields_error' key.
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = self.to_internal_value(data).get('data')
        try:
            self.run_validators(value)
            value = self.validate(value)
            assert value is not None, '.validate() should return the validated data'
        except (serializers.ValidationError, serializers.DjangoValidationError) as exc:
            raise serializers.ValidationError(detail=serializers.as_serializer_error(exc))

        return value

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        """
        if not isinstance(data, serializers.Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise serializers.ValidationError({
                serializers.api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        ret = OrderedDict()
        errors = OrderedDict()
        fields = self._writable_fields

        for field in fields:
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            primitive_value = field.get_value(data)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except serializers.ValidationError as exc:
                errors[field.field_name] = exc.detail
            except serializers.DjangoValidationError as exc:
                errors[field.field_name] = serializers.get_error_detail(exc)
            except SkipField:
                pass
            else:
                serializers.set_value(ret, field.source_attrs, validated_value)

        if errors:
            errors = {
                'error': True,
                'data': errors
            }
            raise serializers.ValidationError(errors)

        return {
            'error': False,
            'data': ret
        }

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return {
            'error': False,
            'data': ret
        }
