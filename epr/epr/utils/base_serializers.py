from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from good_info.models import GoodsModel


class GoodsChoiceSerializer(Serializer):

    #用于反序列化
    keywords=serializers.CharField(label='关键词',required=False)

    #用于序列化和反序列化
    category_id = serializers.IntegerField(label='种类',required=False)
    warehouse_id = serializers.IntegerField(label='种类',required=False)
    number_code = serializers.CharField(label='编号或者批号', required=False)

    #用于序列化
    name = serializers.CharField(label='货品名称',read_only=True)
    specification = serializers.CharField(label='规格', read_only=True)
    model_number = serializers.CharField(label='型号',read_only=True)
    color = serializers.CharField(label='颜色', read_only=True)
    remark = serializers.CharField(label='备注', read_only=True)
    units__basic_name = serializers.CharField(label='单位',read_only=True)
    cur_inventory=serializers.CharField(label='库存',read_only=True)




