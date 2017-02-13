from django.contrib.auth.models import Group
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

from orders.models import OrderForMenupic
from orders.serializers import OrderForMenupicSerializer
from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer

# Create your views here.
class UserAccountViewSet(viewsets.GenericViewSet,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @detail_route(methods=['patch'])
    def deposit(self, request, username=None):
        data = request.data

        add_deposit = data.get('deposit', None)
        # is_increment defaults to False
        is_increment = data.get('is_increment', False)

        if is_increment and add_deposit:
            instance = self.get_object()
            deposit = instance.deposit
            request.data['deposit'] = deposit + add_deposit # F expression ?

        return super(UserAccountViewSet, self).partial_update(request)

class OrderView(generics.GenericAPIView):
    serializer_class = OrderForMenupicSerializer

    def post(self, request):
        data = request.data
        user = request.user
        if 'is_menupic' not in data:
            return self.response_400('is_menupic')
        if data['is_menupic']:
            # user table order_id ? (as same as patch & delete)
            data['user'] = user.pk
            s = OrderForMenupicSerializer(data=data)
            if s.is_valid(raise_exception=True):
                s.save()
        else:
            if 'menuitem_id' not in data:
                return self.response_400('menuitem_id')
            self.order_no_menupic(user, data['menuitem_id'])

        if 'group_id' not in data:
            return self.response_400('group_id')
        self.add_user_to_group(data['group_id'])

        # deposit processing

        return Response(status=status.HTTP_201_CREATED)

    def patch(self, request):
        data = request.data
        user = request.user
        if 'is_menupic' not in data:
            return self.response_400('is_menupic')
        if data['is_menupic']:
            o = OrderForMenupic.objects.get(user=user)
            s = OrderForMenupicSerializer(o, data=data, partial=True)

            if s.is_valid(raise_exception=True):
                s.save()
        else:
            if 'menuitem_id' not in data:
                return self.response_400('menuitem_id')
            self.order_no_menupic(user, data['menuitem_id'])

        # if a user want to switch group, then delete the existed order first.

        # deposit processing

        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        data = request.data
        user = request.user
        if 'is_menupic' not in data:
            return self.response_400('is_menupic')
        if data['is_menupic']:
            o = OrderForMenupic.objects.get(user=user)
            o.delete()
        else:
            self.order_no_menupic(user)

        self.delete_user_from_group(user)

        # deposit processing

        return Response(status=status.HTTP_204_NO_CONTENT)


    def order_no_menupic(self, user, order_id=None):
        if order_id:
            User.objects.all().filter(username=user).update(order=order_id)
        else:
            User.objects.all().filter(username=user).update(order=None)

    def add_user_to_group(self, group_id):
        group = Group.objects.get(pk=group_id)
        group.user_set.add(user)

    def delete_user_from_group(self, user):
        group = user.groups.first()
        group.user_set.remove(user)

    def response_400(self, not_found_field):
        return Response('You should set `' + not_found_field + '` field.',
                        status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
