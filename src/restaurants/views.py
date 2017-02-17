from django.db.models import F
from rest_framework import viewsets, mixins, generics, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from rest_framework.views import APIView
# from rest_framework import permissions
# from django_filters.rest_framework import FilterSet
# from django_filters import rest_framework as filters

from .models import Restaurant, MenuItem
from .serializers import (
    MenuItemRelatedSerializer,
    RestaurantListSerializer,
    RestaurantBesidesListSerializer,
)

class RestaurantViewSet(viewsets.ModelViewSet):
    '''
    Question endpoint

    create:
    Question endpoint

    ---
    required parameter:

    "name": restaurant name

    "menu_picture" or "menu_items": you should specify one of them or both.

    "menu_picture" is a url field, and "menu_items" is a list of menuitem object.
    '''
    queryset = Restaurant.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve') :
            return RestaurantListSerializer
        else:
            return RestaurantBesidesListSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if not data['menu_picture'] and not data['menu_items']:
            return Response('pictures or items (or both) are required when add a restaurant.',
                status=status.HTTP_400_BAD_REQUEST)
        else:
            return super(RestaurantViewSet, self).create(request, *args, **kwargs)

# class MenuItemFilter(filters.FilterSet):
#     restaurant_id = filters.NumberFilter(name='restaurant')
#     class Meta:
#         model = MenuItem
#         fields = ['restaurant_id']


class MenuItemListViewSet(viewsets.GenericViewSet):
    '''
    list:
    restaurants endpoint
    '''
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemRelatedSerializer
    # filter_class = MenuItemFilter

    def list(self, request, restaurant_pk=None):
        menuitems = self.queryset.filter(restaurant=restaurant_pk) # or get_queryset ?
        serializer = MenuItemRelatedSerializer(menuitems, many=True)
        return Response(serializer.data)

class MenuItemBesidesListViewSet(viewsets.GenericViewSet,
                                    mixins.ListModelMixin, # for developing
                                    mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin):
    '''
    menuitems endpoint except GET

    create:
    menuitems endpoint except GET

    ---
    required parameter:

    "name": item name

    "price": item price

    "restaurant": restaurant id

    list:
    This is for developing. please use /restaurants/{restaurant_pk}/menuitems/

    partial_update:
    menuitems endpoint except GET

    ---
    An optional parameter for convenience:

    "is_increment": set to true while specifying "price" field as an addition. default is false.
    '''
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemRelatedSerializer

    def partial_update(self, request, pk=None):
        data = request.data

        add_price = data.get('price', None)
        # is_increment defaults to False
        is_increment = data.get('is_increment', False)

        if is_increment and add_price:
            instance = self.get_object()
            price = instance.price
            request.data['price'] = price + add_price

        return super(MenuItemBesidesListViewSet, self).partial_update(request)

class MenuItemUpdateByRestaurantView(generics.GenericAPIView):
    '''
    patch:
    Update ALL items in a restaurant

    ---
    required parameter:

    "restaurant": restaurant id

    An optional parameter for convenience:

    "is_increment": set to true while specifying "price" field as an addition. default is false.
    '''
    serializer_class = MenuItemRelatedSerializer

    def patch(self, request, *args, **kwargs):
        try:
            data = request.data
            restaurant_id = data['restaurant_id']
            price = data['price']
        except (TypeError, KeyError):
            return Response('You should send an object containing restaurant_id & price to PATCH this url.',
                status=status.HTTP_400_BAD_REQUEST)

        # is_increment defaults to False
        is_increment = data.get('is_increment', False)

        if is_increment:
            MenuItem.objects.filter(restaurant=restaurant_id).update(price=(F('price') + price))
        else:
            MenuItem.objects.filter(restaurant=restaurant_id).update(price=price)
        return Response(status=status.HTTP_200_OK)
