from django.db import transaction
from rest_framework.serializers import ModelSerializer

from sale_info.models import SaleModel,SaleItemModel


class SaleItemSerializer(ModelSerializer):
    class Meta:
        model = SaleItemModel
        fields = '__all__'

class SaleSerializer(ModelSerializer):

    #不可读，若想获得item_list，需要单独查询
    item_list=SaleItemSerializer(many=True,write_only=True)

    class Meta:
        model=SaleModel
        fields='__all__'
    #因为模型嵌套，所以要重写create
    def create(self, validated_data):
        #此处必须用pop，因为是嵌套模型，同时写入会报错
        item_list=validated_data.pop('item_list')
        with transaction.atomic():
            sale=SaleModel.objects.create(**validated_data)
            sale.operator_user_name=sale.operator_user.username
            sale.check_user_name=sale.check_user.username
            sale.customer_name=sale.customer.name
            for item in item_list:
                saleitem=SaleItemModel.objects.create(sale=sale,**item)
                good=item.get('goods')
                saleitem.specification=good.specification
                saleitem.model_number=good.model_number
                saleitem.color=good.color
                saleitem.units_name=good.units.basic_name
                saleitem.save()
        return sale
    #重写update，将saleitem部分全部删除重新添加，其余部分正常修改
    def update(self, instance, validated_data):
        item_list=validated_data.pop('item_list')
        old_list=instance.item_list
        if old_list.exists():
            old_list.all().delete()
        with transaction.atomic():
            for item in item_list:
                saleitem=SaleItemModel.objects.create(**item,sale=instance)
                good = item.get('goods')
                print('good------------>',good.specification)
                saleitem.specification = good.specification
                saleitem.model_number = good.model_number
                saleitem.color = good.color
                saleitem.units_name = good.units.basic_name
                saleitem.save()
            sale=super(SaleSerializer, self).update(instance=instance,validated_data=validated_data)
            sale.operator_user_name = sale.operator_user.username
            sale.check_user_name = sale.check_user.username
            sale.customer_name = sale.customer.name
            sale.save()
        return sale

class SaleSearchSerializer(ModelSerializer):

    item_list=SaleItemSerializer(read_only=True,many=True)

    class Meta:
        model=SaleModel
        fields='__all__'




