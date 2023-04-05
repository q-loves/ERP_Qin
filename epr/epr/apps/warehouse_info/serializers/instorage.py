from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from warehouse_info.models import PurchaseStorageModel, PurchaseStorageItemModel


class InStorageItemSerializer(ModelSerializer):

    class Meta:
        model=PurchaseStorageItemModel
        fields='__all__'


class InStorageSerializer(ModelSerializer):

    item_list=InStorageItemSerializer(many=True,write_only=True)

    class Meta:
        model = PurchaseStorageModel
        fields='__all__'

    #因为新增时，要增加入库表单和具体的入库项目，所以要重写create
    def create(self, validated_data):
        item_list=validated_data.pop('item_list')
        with transaction.atomic():
            pur=PurchaseStorageModel.objects.create(**validated_data)
            for item in item_list:
                good=item.get('goods')
                units=item.get('units')
                warehouse=item.get('warehouse')
                pui=PurchaseStorageItemModel.objects.create(**item,purchase_storage=pur)
                #自动添加冗余字段
                pui.name=good.name
                pui.color=good.color
                pui.specification=good.specification
                pui.specification=good.specification
                pui.units_name=units.basic_name
                pui.warehouse_name=warehouse.name
                pui.save()
        return pur
    #删掉原来的入库项目重新填写，入库表正常修改
    def update(self, instance, validated_data):
        item_list=validated_data.pop('item_list')
        old_list=instance.item_list.all()
        if old_list.exists():
            old_list.delete()
        for item in item_list:
            good = item.get('goods')
            units = item.get('units')
            warehouse = item.get('warehouse')
            pui = PurchaseStorageItemModel.objects.create(**item, purchase_storage=instance)
            # 自动添加冗余字段
            pui.name = good.name
            pui.color = good.color
            pui.specification = good.specification
            pui.specification = good.specification
            pui.units_name = units.basic_name
            pui.warehouse_name = warehouse.name
            pui.save()
        return super(InStorageSerializer, self).update(instance=instance,validated_data=validated_data)

class InStorageSearchSerializer(ModelSerializer):

    item_list=serializers.SerializerMethodField()

    class Meta:
        model=PurchaseStorageModel
        fields='__all__'
    def get_item_list(self,obj):
        result=[]
        item_list=obj.item_list.all()
        for item in item_list:
            dict={}
            good=item.goods
            warehouse=item.warehouse
            dict['name']=good.name
            dict['number_code']=good.number_code
            dict['units_name']=good.units.basic_name
            dict['warehouse_name']=warehouse.name
            result.append(dict)
        return result




