from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from good_info.models import UnitsModel


class UnitsSerializer(ModelSerializer):

    units_name=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=UnitsModel
        fields='__all__'

    def  get_units_name(self,obj):
        return str(obj)
