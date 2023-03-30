from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from basic_info.models import SettlementAccountModel

from basic_info.serializers.settlement_account import SettlementAccountSerializer

from epr.utils.get_queryset_by_keywords import GetQuerysetByKeywords


class SettlementAccountView(ModelViewSet,GetQuerysetByKeywords):
    queryset = SettlementAccountModel.objects.all()
    serializer_class = SettlementAccountSerializer

    keywords=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
        'name':openapi.Schema(type=openapi.TYPE_STRING),
        'number_code':openapi.Schema(type=openapi.TYPE_STRING),
        'remark':openapi.Schema(type=openapi.TYPE_STRING),
    })
    @swagger_auto_schema(method='post',request_body=keywords,operation_description='传入关键字查询')
    @action(methods=['post'],detail=False)
    def get_queryset_by_keywords(self,request,*args,**kwargs):
        name = request.data.get('name')
        number_code = request.data.get('number_code')
        remark = request.data.get('remark')
        q = Q()
        if name:
            q.add(Q(name__contains=name), 'AND')
        if number_code:
            q.add(Q(phone__contains=number_code), 'AND')
        if remark:
            q.add(Q(city__contains=remark), 'AND')
        pur_queryset = SettlementAccountModel.filter(q).all()

        data = SettlementAccountSerializer(instance=pur_queryset, many=True).data
        return Response(data)
