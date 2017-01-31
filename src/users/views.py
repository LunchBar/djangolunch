from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer

# Create your views here.
class UserViewSet(viewsets.GenericViewSet,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def partial_update(self, request, pk=None):
        data = request.data

        add_deposit = data.get('deposit', None)
        # is_increment defaults to False
        is_increment = data.get('is_increment', False)
        is_true = lambda value: bool(value) and value.lower() not in ('false', '0')

        if is_true(is_increment) and add_deposit:
            instance = self.get_object()
            deposit = instance.deposit
            request.data['deposit'] = deposit + add_deposit

        return super(UserViewSet, self).partial_update(request)

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
