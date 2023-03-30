from rest_framework.serializers import ModelSerializer

from basic_info.models import SettlementAccountModel


class SettlementAccountSerializer(ModelSerializer):

    class Meta:
        model=SettlementAccountModel
        fields='__all__'