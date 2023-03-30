from rest_framework.fields import IntegerField, BooleanField
from rest_framework.serializers import ModelSerializer, Serializer

from erp_system.models import RoleModel

from erp_system.models import PermissionModel

from erp_system.serializers.permission import PermissionSerializer


class RoleSimpleSerializer(ModelSerializer):
    #查询角色内容时，详细展示permission
    permission=PermissionSerializer(many=True,read_only=True)

    class Meta:
        model=RoleModel
        fields='__all__'

class RolePartialSerializer(Serializer):

    role_id=IntegerField(write_only=True,required=True)
    permission_id=IntegerField(write_only=True,required=True)
    is_create=BooleanField(write_only=True,required=True)

class RolesPartialSerializer(ModelSerializer):

    class Meta:
        model=RoleModel
        fields=['id','permission']