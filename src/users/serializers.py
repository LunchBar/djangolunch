from rest_framework import serializers

from orders.serializers import OrderSerializer
from restaurants.serializers import MenuItemRelatedSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)
    group_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'deposit', 'orders', 'group_id') # put Chinese name in first_name

    def get_group_id(self, obj):
        group = obj.groups.first()
        if not group:
            return None
        else:
            return group.pk

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
