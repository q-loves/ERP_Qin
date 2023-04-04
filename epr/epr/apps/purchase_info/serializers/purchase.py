from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from purchase_info.models import PurchaseModel,PurchaseItemModel

from good_info.models import GoodsModel


class PurchaseItemSerializer(ModelSerializer):

    class Meta:
        model=PurchaseItemModel
        fields='__all__'

class PurchaseSerializer(ModelSerializer):

    item_list=PurchaseItemSerializer(many=True,write_only=True)
    goods_info=serializers.SerializerMethodField()

    class Meta:
        model=PurchaseModel
        fields='__all__'

    def create(self, validated_data):
        item_list=validated_data.pop('item_list')
        with transaction.atomic():#数据库事务处理
            purchase=PurchaseModel.objects.create(**validated_data)
            for item in item_list:
                pim=PurchaseItemModel.objects.create(**item,purchase=purchase)
                #如果前段不把冗余字段传过来，那将自动填入
                good=item.get('goods')
                pim.name=good.name
                pim.specification=good.specification
                pim.number_code=good.number_code
                pim.save()
        return purchase
    #重写update，每次修改时，所有订单全部删除，再重新选择
    def update(self, instance, validated_data):
        old_list=instance.item_list
        new_list=validated_data.pop('item_list')
        status=instance.status
        if status != '0':
            raise ValidationError('该订单已审核通过，不可修改')
        if old_list.exists():
            instance.item_list.all().delete()
        for item in new_list:
            pim=PurchaseItemModel.objects.create(**item,purchase=instance)
            #如果前段不把冗余字段传过来，那将自动填入
            good=item.get('goods')
            pim.name=good.name
            pim.specification=good.specification
            pim.number_code=good.number_code
            pim.save()
        return super(PurchaseSerializer, self).update(instance=instance,validated_data=validated_data)

    def get_goods_info(self,obj):
        if obj.item_list:
            result=[]
            for item in obj.item_list.all():
                result.append(item.name + (item.specification if item.specification else '') +item.number_code)
            return ','.join(result)
        return ''

#用于展示某一个订单的具体购买货物信息
class PurchaseGetItemSerializer(ModelSerializer):

    item_list=serializers.SerializerMethodField()

    class Meta:
        model=PurchaseModel
        fields='__all__'

    def get_item_list(self,obj):
        result=[]
        if obj.item_list.all():
            for item in obj.item_list.all():
                dict={}
                # good=GoodsModel.objects.get(id=item.goods.id)
                good=item.goods
                dict['name']=good.name
                dict['specification']=good.specification
                dict['model_number']=good.model_number
                dict['color']=good.color
                dict['basic_weight']=good.basic_weight
                dict['expiration_day']=good.expiration_day
                dict['remark']=good.remark
                dict['number_code']=good.number_code
                dict['purchase_price']=good.purchase_price
                dict['retail_price']=good.retail_price
                dict['sales_price']=good.sales_price
                dict['lowest_price']=good.lowest_price
                dict['order_number']=good.order_number
                result.append(dict)
            return result
        return result





            
            








