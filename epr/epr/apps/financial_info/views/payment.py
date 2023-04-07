from django.db import transaction
from django.db.models import Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from financial_info.models import PaymentModel,PaymentItemModel

from financial_info.serializers.payment import PaymentSerializer

from purchase_info.models import PurchaseModel

from warehouse_info.models import PurchaseStorageModel

from epr.utils.base_views.multiple_delete import MultipleDeleteMixin


class PaymentView(ModelViewSet,MultipleDeleteMixin):

    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSerializer
    """
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
                pay_category=payment.pay_category
                if pay_category=='1':#付定金
                    pur=PurchaseModel.objects.get(payment__id=payment.id)
                    pur.status='5'
                    pur.save()
                if pay_category=='2':#按照入库单付款
                    payment_items=PaymentItemModel.objects.filter(payment_id=payment.id)
                    #将关联的入库单全部提取出来
                    for item in payment_items:
                        instorage=PurchaseStorageModel.objects.get(payment_item__id=item.id)
                        instorage.this_payment=item.this_money
                        instorage.this_debt=instorage.last_amount-instorage.this_payment
                        if not instorage.this_debt:#判断入库单是否还有欠款,填入入库单状态
                            instorage.status='3'
                            instorage.save()
                        instorage.status='2'
                        instorage.save()
                #判断采购单是否还有欠款last_amount 和 deposit
                pur=PurchaseModel.objects.get(payment__id=payment.id)
                #将该采购单对应的所有支付单的已付金额进行求和
                pay_money=PaymentModel.objects.filter(purchase_id=pur.id).aggregate(sum=Sum('pay_money'))
                if pay_money['sum']==pur.last_amount:
                    pur.status='5'#全部付款完成
                    pur.save()
        return Response(data={'message':'审批成功'})








