from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from good_info.models import GoodsCategoryModel


class GoodsCategorySerializer(ModelSerializer):

    children=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=GoodsCategoryModel
        fields='__all__'

    def get_children(self,obj):
        if obj.children:
            return GoodsCategorySerializer(instance=obj.children,many=True).data
        return None
