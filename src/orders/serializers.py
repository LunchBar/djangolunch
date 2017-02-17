from django.db import models
from rest_framework import serializers

from restaurants.models import Restaurant
from .models import OrderForMenupic, OrderGroup

class OrderForMenupicSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderForMenupic
        fields = ['user', 'name', 'price']

class OrderGroupBesidesListSerializer(serializers.ModelSerializer):
    name = models.CharField(max_length=20)
    class Meta:
        model = OrderGroup
        fields = ['leader', 'restaurant', 'name']

class OrderGroupListSerializer(serializers.ModelSerializer):
    leader = serializers.SlugRelatedField(
        read_only=True,
        # queryset=GroupMember.objects.all(),
        slug_field='first_name',
    )
    class Meta:
        model = OrderGroup
        fields = ['id', 'leader', 'restaurant', 'name']
