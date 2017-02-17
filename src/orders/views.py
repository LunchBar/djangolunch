from django.contrib.auth.models import Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from restaurants.models import Restaurant
from .models import OrderGroup
from .serializers import OrderGroupListSerializer, OrderGroupBesidesListSerializer

# Create your views here.
class OrderGroupViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin):
    '''
    order group endpoint.

    create:
    order group endpoint.

    ---
    required parameter:

    "restaurant": selected restaurant id

    "name": selected restaurant name
    '''
    queryset = OrderGroup.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve') :
            return OrderGroupListSerializer
        else:
            return OrderGroupBesidesListSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        restaurant_name = Restaurant.objects.get(pk=data['restaurant']).name

        request.data['name'] = restaurant_name
        request.data['leader'] = request.user.pk
        return super(OrderGroupViewSet, self).create(request, *args, **kwargs)
