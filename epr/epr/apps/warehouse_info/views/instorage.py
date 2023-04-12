from django.db import transaction
from django.db.models import Sum, F
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from warehouse_info.models import PurchaseStorageModel


from warehouse_info.serializers.instorage import InStorageSerializer

from warehouse_info.serializers.instorage import InStorageSearchSerializer

from purchase_info.models import PurchaseModel

from basic_info.models import SupplierModel

from good_info.models import GoodsInventoryModel

from epr.utils.base_views.multiple_delete import MultipleDeleteMixin


class InStorageView(ModelViewSet,MultipleDeleteMixin):

    queryset = PurchaseStorageModel.objects.all()
    serializer_class = InStorageSerializer
    def get_serializer_class(self):
        if self.action=='retrieve':
            return InStorageSearchSerializer
        return InStorageSerializer

    """ 
    审批入库订单
    1.与采购订单所关联的订单，状态必须时1,2,5才可以进行审批
    2.审批后要将关联的采购订单状态修改为 部分入库或全部入库
    3.如果有欠款，那么供应商的 期末应付+=欠款
    4.相关货物的库存+=入库数量
     """
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
        'ids':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER),description='输入入库单号')
    })
    @swagger_auto_schema(method='put',request_body=request_body,operation_description='输入要审批的入库单号')
    @action(methods=['put'],detail=False)
    def multiple_audit(self,request,*args,**kwargs):
        with transaction.atomic():
            ids=request.data.get('ids')
            psm=PurchaseStorageModel.objects.filter(id__in=ids).all()
            if len(ids) > psm.count():
                return Response(data={'message':'要审核的数据不存在'})
            for pus in psm:

                #计算欠款
                current_pay=pus.purchase.supplier.current_pay
                this_debt=pus.this_debt
                if not this_debt:
                    this_debt=0
                SupplierModel.objects.filter(id=pus.supplier.id).update(current_pay=F('current_pay')+this_debt)
                #计算货物库存
                for item in pus.item_list.all():
                    goods_add=item.purchase_count
                    GoodsInventoryModel.objects.filter(goods_id=item.goods.id,warehouse_id=item.warehouse.id).update(cur_inventory=F('cur_inventory')+goods_add)
                #判断是否与采购订单关联
                if pus.purchase:

                    if pus.purchase.status=='3' or pus.purchase.status=='4':
                        raise ValidationError('该订单已完成，不可修改')
                    #计算是否全部入库
                    in_count_now=pus.number_count
                    in_count_before=PurchaseStorageModel.objects.filter(purchase_id=pus.purchase.id).exclude(status='0').aggregate(sum=Sum('number_count'))

                    total_count=pus.purchase.number_count

                    if in_count_now+(in_count_before['sum'] if in_count_before['sum'] else 0) == total_count:
                        pus.purchase.status='3'
                    else:
                        pus.purchase.status='2'
                    pus.purchase.save()
                pus.status='1'
                pus.save()
        return Response(data={'message':'审批成功'},status=status.HTTP_200_OK)



