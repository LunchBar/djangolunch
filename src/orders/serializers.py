from django.db import models
from rest_framework import serializers

from .models import OrderForMenupic

# Cleanup ??

class OrderForMenupicSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderForMenupic
        fields = ['user', 'name', 'price']



#########################################################################
# class MenuItemRelatedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MenuItem
#         fields = ['id', 'name', 'price', 'restaurant']

# class RestaurantListSerializer(serializers.ModelSerializer):
#     # not merely 'list' but 'retrieve' use it lol

#     # menu_items = MenuItemRelatedSerializer(many=True)
#     # menu_items = serializers.HyperlinkedRelatedField(
#     #     many=True,
#     #     # read_only=True,
#     #     queryset=MenuItem.objects.all(),
#     #     view_name='menuitem-list'
#     # )
#     menu_items_url = serializers.HyperlinkedIdentityField(
#         view_name='menuitem-list',
#         lookup_url_kwarg='restaurant_pk'
#     )

#     class Meta:
#         model = Restaurant
#         fields = ['id', 'name', 'address', 'note', 'menu_picture', 'menu_items_url']

# class RestaurantBesidesListSerializer(serializers.ModelSerializer):
#     menu_items = MenuItemRelatedSerializer(many=True) # ????????????????
#     class Meta:
#         model = Restaurant
#         fields = ['name', 'address', 'note', 'menu_picture', 'menu_items']
#         extra_kwargs = {'menu_items': {'required': False}}

#     def create(self, validated_data):
#         menu_items = validated_data.pop('menu_items')

#         restaurant = Restaurant.objects.create(**validated_data)

#         # print(menu_items[0]['name'])
#         for menu_item in menu_items:
#             menu_item['restaurant'] = restaurant
#         bulk_menuitems = [MenuItem(**menu_item) for menu_item in menu_items]
#         # print(bulk_menuitems)
#         MenuItem.objects.bulk_create(bulk_menuitems)

#         # for menu_item in menu_items:
#         #     MenuItem.objects.create(restaurant=restaurant, **menu_item)

#         return restaurant
