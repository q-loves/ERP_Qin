from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from good_info.models import GoodsModel

from good_info.models import GoodsInventoryModel

from good_info.serializers.units import UnitsSerializer

from good_info.serializers.goodscategory import GoodsCategorySerializer

from good_info.models import AttachmentModel

from good_info.serializers.attachment import AttachmentSerializer

from epr.utils.base_views.get_cur_inventory import  get_current_inventory


class GoodsInventorySerializer(ModelSerializer):

    class Meta:
        model=GoodsInventoryModel
        fields='__all__'


class GoodsSimpleSerializer(ModelSerializer):

    inventory_list=GoodsInventorySerializer(many=True,required=True)

    class Meta:
        model=GoodsModel
        fields='__all__'
    #重写create,在增加商品时，加上初始库存
    def create(self, validated_data):
        inventory_list=validated_data.pop('inventory_list')
        with transaction.atomic():#数据库事务处理
            goods=GoodsModel.objects.create(**validated_data)
            for item in inventory_list:
                item['cur_inventory']=item.get('init_inventory',0)
                GoodsInventoryModel.objects.create(goods=goods,**item)
        return goods
    #重写update，在修改时只能修改库存的最大值最小值
    def update(self, instance, validated_data):
        inventory_list=validated_data.pop('inventory_list')
        for item in inventory_list:
            GoodsInventoryModel.objects.filter(goods=instance.id,warehouse_name=item['warehouse_name']).update(
                lowest_inventory=item.get('lowest_inventory',0),highest_inventory=item.get('highest_inventory',0))
            goods=super(GoodsSimpleSerializer, self).update(instance=instance,validated_data=validated_data)
            return goods


class GoodsSearchSerializer(ModelSerializer):

    units=UnitsSerializer(read_only=True)
    categories=GoodsCategorySerializer(read_only=True)
    image_list=serializers.SerializerMethodField()

    inventory_list=GoodsInventorySerializer(read_only=True,many=True)
    category=serializers.SlugRelatedField(slug_field='name',read_only=True)
    cur_inventory=serializers.SerializerMethodField()
    class Meta:
        model=GoodsModel
        fields='__all__'

    def get_image_list(self,obj):
        result=[]
        if obj.images_list:
            ids=obj.images_list.split(',')
            for id in ids:
                image=AttachmentModel.objects.get(id=id)
                data=AttachmentSerializer(instance=image).data
                result.append(data)
        return result

    def get_cur_inventory(self,obj):
        return get_current_inventory(obj.id)













