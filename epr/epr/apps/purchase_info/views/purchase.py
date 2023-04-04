from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from purchase_info.models import PurchaseModel

from purchase_info.serializers.purchase import PurchaseSerializer

from purchase_info.serializers.purchase import PurchaseGetItemSerializer
from epr.utils.base_views.get_queryset_by_keywords import GetQuerysetByKeywords
from epr.utils.base_views.multiple_audit import MultipleAuditMixin


class PurchaseView(ModelViewSet,MultipleAuditMixin,GetQuerysetByKeywords):

    queryset = PurchaseModel.objects.all()

    def get_serializer_class(self):
        if self.action=='retrieve':
            return PurchaseGetItemSerializer
        return PurchaseSerializer

    params=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
        'check_user_name':openapi.Schema(type=openapi.TYPE_STRING,description='审核人的用户名'),
        'supplier_name':openapi.Schema(type=openapi.TYPE_STRING,description='供应商的用户名'),
        'operator_user_name':openapi.Schema(type=openapi.TYPE_STRING,description='操作人员的用户名'),
        'number_code':openapi.Schema(type=openapi.TYPE_STRING,description='编号'),
    })
    @swagger_auto_schema(methods=['post'], request_body=params, operation_description='传入关键词查询订单')
    @action(methods=['post'], detail=False)
    def get_queryset_by_keywords(self, request, *args, **kwargs):
        check_user_name = request.data.get('check_user_name')
        supplier_name = request.data.get('supplier_name')
        operator_user_name = request.data.get('operator_user_name')
        number_code = request.data.get('number_code')
        status = request.data.get('status')
        q = Q()
        if check_user_name:
            q.add(Q(check_user_name__contains=check_user_name), 'AND')
        if supplier_name:
            q.add(Q(supplier_name__contains=supplier_name), 'AND')
        if operator_user_name:
            q.add(Q(operator_user_name__contains=operator_user_name), 'AND')
        if number_code:
            q.add(Q(number_code__contains=number_code), 'AND')
        if status:
            q.add(Q(status=status),'AND')
        pur = PurchaseModel.objects.filter(q)
        data = PurchaseSerializer(instance=pur, many=True).data
        return Response(data)

