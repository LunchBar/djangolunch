from django.contrib.auth.models import Group
from django.db.models import F, CharField
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.aggregates import Count, Sum
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from restaurants.models import Restaurant
from .models import OrderGroup, Order
from .serializers import (
    OrderGroupListSerializer,
    OrderGroupBesidesListSerializer,
    OrderSerializer,
    NoteDetailSerializer,
)

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

    @detail_route(methods=['get'])
    def orders(self, request, pk=None):
        '''
        (for group leader) check out group orders
        '''
        data = {}

        group = self.get_object()
        group_orders = group.orders

        # for developing only?
        s = NoteDetailSerializer(group_orders.all(), many=True)
        data['note_detail'] = s.data

        data['orders'] = group_orders.values('name').annotate(note=ArrayAgg('note'), amount=Sum('amount')).order_by()

        total_dict = group_orders.aggregate(total_price=Sum(F('price') * F('amount')), total_amount=Sum(F('amount')))
        data.update(total_dict)

        return Response(data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin, # for developing
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    '''
    orders endpoint except GET

    list:
    This is for developing. please use /account/{username}/ to check personal order

    create:
    orders endpoint except GET

    ---
    required parameter:

    "name", "price", "amount": trivial

    "group": group id that orders belong to
    '''
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create(self, request):
        data = request.data
        user = request.user

        if 'group' not in data:
            return self.response_400('group')
        self.add_user_to_group(user, data['group'])

        # TODO: deposit processing (as same as patch & delete)

        data['user'] = user.pk
        return super(OrderViewSet, self).create(request)

    def destroy(self, request, pk=None):
        user = request.user
        group = self.get_object().group

        if Order.objects.filter(user=user, group=group).count() == 1:
            self.delete_user_from_group(user, group)

        return super(OrderViewSet, self).destroy(request)

    def add_user_to_group(self, user, group_id):
        group = Group.objects.get(pk=group_id)
        group.user_set.add(user)

    def delete_user_from_group(self, user, group):
        group.user_set.remove(user)

    def response_400(self, not_found_field): # TODO: move to util?
        return Response('You should set `' + not_found_field + '` field.',
                        status=status.HTTP_400_BAD_REQUEST)
