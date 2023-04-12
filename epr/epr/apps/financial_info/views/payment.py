from django.db import transaction
from django.db.models import Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from financial_info.models import PaymentModel,PaymentItemModel

from financial_info.serializers.payment import PaymentSerializer

from purchase_info.models import PurchaseModel

from warehouse_info.models import PurchaseStorageModel

from basic_info.models import SettlementAccountModel
from epr.utils.base_views.multiple_delete import MultipleDeleteMixin


class PaymentView(ModelViewSet,MultipleDeleteMixin):

    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSerializer
    """
    审核条件
    1.绑定的采购单状态不可为0
    2.绑定的入库单状态为已审核
    3.支付用户的余额要大于或等于付款金额
    4.采购单对应的入库单必须全部入库，并且全部付款完成，才可以将其状态改为采购完成
    注：定金支付单只能单独审批，因定金支付完成后，期所对应的采购单状态会为5，此时要审批入库单，才可修改采购单的状态为部分入库或全部入库
    审核需求
    1.若要付定金，付款完成后要修改关联采购单的状态
    2.若要按照入库单付款，需要修改入库单状态，部分付款或全部付款，
      并且要判断关联的采购单是否已经完成付款
    3.如果要支付欠款，需要修改supplier的current_pay属性
    4.最后要修改支付账户account的余额  
    """
    ids=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
        'ids':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER),description='传入要审批的支付单的ids')
    })
    @swagger_auto_schema(method='post',request_body=ids,operation_description='传入要审批的支付单的ids')
    @action(methods=['POST'],detail=False)
    def multiple_audit(self,request,*args,**kwargs):
        with transaction.atomic():
            ids=request.data.get('ids')
            payments=PaymentModel.objects.filter(id__in=ids).all()
            for payment in payments:
                # if payment.status=='1':#表单不可反审核
                #     raise ValidationError(f'id为{payment.id}的表单已经被审核')
                pay_category=payment.pay_category
                if pay_category=='1':#付定金
                    pur=payment.purchase
                    pur.status='5'
                    pur.save()
                    return Response(data={'message':'定金支付单不可与其他支付单一同进行审批，请将其他表单另外进行审批'})
                if pay_category=='2':#按照入库单付款
                    payment_items=PaymentItemModel.objects.filter(payment_id=payment.id).all()
                    #将关联的入库单全部提取出来
                    for item in payment_items:
                        instorage=PurchaseStorageModel.objects.get(payment_item__id=item.id)
                        if instorage.status=='0':
                            raise ValidationError(f'id为{instorage.id}的入库单未审核，不可进行支付')
                        if instorage.status=='3':
                            raise ValidationError(f'id为{instorage.id}的入库单以完成付款，不可进行支付')
                        #因为每个入库单可以进行多次付款，所以每次付款都要加上之前的金额
                        instorage.this_payment=(instorage.this_payment if instorage.this_payment else 0)+item.this_money
                        instorage.this_debt=instorage.last_amount-instorage.this_payment
                        if not instorage.this_debt:#判断入库单是否还有欠款,填入入库单状态
                            instorage.status='3'
                            instorage.save()
                        instorage.status='2'
                        instorage.save()
                #判断采购单是否还有欠款last_amount 和 deposit
                pur=PurchaseModel.objects.get(payment__id=payment.id)
                #将该采购单对应的所有已审核过的支付单的已付金额进行求和
                pay_money=PaymentModel.objects.filter(purchase_id=pur.id).exclude(status='0').aggregate(sum=Sum('pay_money'))
                # if (pay_money['sum'] if pay_money['sum'] else 0)+payment.pay_money  ==pur.last_amount:
                pus_count=PurchaseStorageModel.objects.filter(purchase_id=pur.id).exclude(status='3').count()#将入库单中所有未付款完成的统计出来
                if pur.status=='3' and not pus_count:
                    pur.status='4'#全部付款完成
                    pur.save()
                if (pay_money['sum'] if pay_money['sum'] else 0) + payment.pay_money > pur.last_amount:
                    raise ValidationError(f'id为{pur.id}的采购单已经完成支付，不可再进行支付')
                #修改payment状态，改为已审核
                payment.status='1'
                payment.save()
                #修改支付用户的余额
                account=payment.account
                account.balance=account.balance-payment.pay_money
                account.save()
                if account.balance<0:
                    raise ValidationError(f'id为{account.id}的支付账户余额不足')

        return Response(data={'message':'审批成功'})








