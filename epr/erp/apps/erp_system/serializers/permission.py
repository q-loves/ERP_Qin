from rest_framework.serializers import ModelSerializer

from erp_system.models import PermissionModel


class PermissionSerializer(ModelSerializer):

    class Meta:
        model=PermissionModel
        fields='__all__'