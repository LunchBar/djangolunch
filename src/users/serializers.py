from rest_framework import serializers

from orders.serializers import OrderSerializer
from restaurants.serializers import MenuItemRelatedSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'deposit', 'orders') # put Chinese name in first_name

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
