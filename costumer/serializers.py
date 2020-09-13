from rest_framework import serializers
from django.contrib.auth import get_user_model

from extended_lib.rest_framework.serializers import ModelSerializer
from extended_lib.rest_framework.validators import UniqueValidator
from costumer.models import Costumer

User = get_user_model()


class CostumerSerializer(ModelSerializer):
    phone = serializers.ReadOnlyField(
        label='تلفن همراه',
        source='user.phone'
    )
    email = serializers.EmailField(
        label='ایمیل',
        source='user.email',
        allow_blank=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        label='نام',
        source='user.first_name',
        max_length=30,
        allow_blank=True
    )
    last_name = serializers.CharField(
        label='نام خانوادگی',
        source='user.last_name',
        max_length=150,
        allow_blank=True
    )

    class Meta:
        model = Costumer
        exclude = ['bank_card', 'user']
        extra_kwargs = {
            'national_code': {
                'label': 'کد ملی'
            },
            'birth_day': {
                'label': 'تاریخ تولد'
            },
            'job': {
                'label': 'شغل'
            },
            'bank_card': {
                'label': 'شماره کارت بانکی'
            }
        }

    def update(self, instance, validated_data):
        if validated_data.get('user'):
            user = validated_data.pop('user')
            instance.user.first_name = user.pop('first_name', instance.user.first_name)
            instance.user.last_name = user.pop('last_name', instance.user.last_name)
            instance.user.email = user.pop('email', instance.user.email)
            instance.user.save()
        return super(CostumerSerializer, self).update(instance, validated_data)
