from rest_framework.serializers import ModelSerializer

from basic_info.models import SupplierModel


class SupplierSerializer(ModelSerializer):

    class Meta:
        model=SupplierModel
        fields='__all__'
