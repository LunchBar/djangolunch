from django.db import models
from rest_framework import serializers

from restaurants.models import Restaurant
from .models import Order, OrderGroup

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'group', 'name', 'price', 'amount', 'note']

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

class NoteDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='first_name',
    )
    class Meta:
        model = Order
        fields = ['user', 'name', 'amount', 'note']
