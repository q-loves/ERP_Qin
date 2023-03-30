from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from basic_info.models import WarehouseModel

#用于增删改
from epr.utils.get_queryset_by_keywords import GetQuerysetByKeywords


class WarehouseSimpleSerializer(ModelSerializer):

    class Meta:
        model=WarehouseModel
        fields='__all__'

#用于查询时可以返回仓库管理人的真实姓名
class WarehouseSearchSerializer(ModelSerializer):

    leader_user=serializers.SlugRelatedField(slug_field='username',read_only=True)

    class Meta:
        model=WarehouseModel
        fields='__all__'