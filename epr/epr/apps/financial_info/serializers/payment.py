from django.db import transaction
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from financial_info.models import PaymentModel, PaymentItemModel


class PaymentItemSerializer(ModelSerializer):

    this_debt=serializers.SerializerMethodField()

    class Meta:
        model=PaymentItemModel
        fields='__all__'

    def get_this_debt(self,obj):
        return obj.should_money-obj.this_money

class PaymentSerializer(ModelSerializer):
    '''
    1.定金支付
    2.与采购单关联的入库支付
    3.欠款支付
    '''
    #1,3不需要多次入库支付，所以不需要item_list
    item_list=PaymentItemSerializer(many=True,required=False)
    total_debt=serializers.SerializerMethodField()
    class Meta:
        model=PaymentModel
        fields='__all__'

    def get_total_debt(self,obj):
        if obj.item_list.all():
            should_money=PaymentItemModel.objects.filter(payment_id=obj.id).aggregate(sum=Sum('should_money'))
            this_money=PaymentItemModel.objects.filter(payment_id=obj.id).aggregate(sum=Sum('this_money'))
            total_debt=should_money['sum']-this_money['sum']
            return total_debt
        return 0


    def create(self, validated_data):
        supplier=validated_data.get('supplier')
        operator_user=validated_data.get('operator_user')
        check_user=validated_data.get('check_user')
        pay_category=validated_data.get('pay_category')
        with transaction.atomic():
            if pay_category!='2' and validated_data.get('item_list'):
                raise ValidationError('该类型的订单不可添加item_list属性')
            if not validated_data.get('item_list'):
                pay = PaymentModel.objects.create(**validated_data)
                pay.operator_user_name = operator_user.username
                pay.check_user_name = check_user.username
                pay.supplier_name = supplier.name
                pay.save()
                return pay
            item_list=validated_data.pop('item_list')
            pay=PaymentModel.objects.create(**validated_data)
            #自动添加冗余字段
            pay.operator_user_name=operator_user.username
            pay.check_user_name=check_user.username
            pay.supplier_name=supplier.name
            pay.save()
            for item in item_list:
                PaymentItemModel.objects.create(**item,payment=pay)
        return pay
    def update(self, instance, validated_data):
        supplier = validated_data.get('supplier')
        operator_user = validated_data.get('operator_user')
        check_user = validated_data.get('check_user')
        pay_category = validated_data.get('pay_category')

        if pay_category != '2' and validated_data.get('item_list'):
            raise ValidationError('该类型的订单不可添加item_list属性')
        if instance.status=='1':
            raise ValidationError('该付款单已被审核，不可再修改')

        with transaction.atomic():
            if not validated_data.get('item_list'):
                instance.operator_user_name = operator_user.username
                instance.check_user_name = check_user.username
                instance.supplier_name = supplier.name
                instance.save()
                return super(PaymentSerializer, self).update(instance=instance,validated_data=validated_data)
            old_list=instance.item_list
            new_list=validated_data.pop('item_list')
            #修改冗余字段
            instance.operator_user_name=operator_user.username
            instance.check_user_name=check_user.username
            instance.supplier_name=supplier.name
            instance.save()
            if old_list.exists():
                instance.item_list.all().delete()
            for item in new_list:
                PaymentItemModel.objects.create(**item,payment=instance)
        return super(PaymentSerializer, self).update(instance=instance,validated_data=validated_data)





