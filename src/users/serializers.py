from rest_framework import serializers

from restaurants.serializers import MenuItemRelatedSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    order = MenuItemRelatedSerializer()
    group_id = serializers.SerializerMethodField()
    # group = serializers.SlugRelatedField(
    #     read_only=True,
    #     # queryset=GroupMember.objects.all(),
    #     slug_field='group_id',
    # )

    class Meta:
        model = User
        fields = ('username', 'username', 'first_name', 'deposit', 'order', 'group_id') # put Chinese name in first_name

    def get_group_id(self, obj):
        print(obj)
        group = obj.groups.first()
        if not group:
            return None
        else:
            return group.pk

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
