from rest_framework.serializers import ModelSerializer

from basic_info.models import CustomerModel


class CustomerSerializer(ModelSerializer):

    class Meta:
        model=CustomerModel
        fields='__all__'