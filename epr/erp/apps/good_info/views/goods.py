from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from good_info.models import GoodsModel

from good_info.serializers.goods import GoodsSimpleSerializer

from good_info.serializers.goods import GoodsSearchSerializer
from erp.utils.get_queryset_by_keywords import GetQuerysetByKeywords


class GoodsView(ModelViewSet,GetQuerysetByKeywords):

    queryset = GoodsModel.objects.all()
    def get_serializer_class(self):
        if self.action=='get_queryset_by_keywords':
            return GoodsSearchSerializer
        else:
            return GoodsSimpleSerializer

    params=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
        'name':openapi.Schema(type=openapi.TYPE_STRING),
        'color':openapi.Schema(type=openapi.TYPE_STRING),
        'number_code':openapi.Schema(type=openapi.TYPE_STRING,description='编号'),
        'category':openapi.Schema(type=openapi.TYPE_STRING,description='类别id'),

    })
    @swagger_auto_schema(request_body=params,operation_description='传入关键词，查询商品详细信息')
    @action(methods=['POST'],detail=False)
    def get_queryset_by_keywords(self,request,*args,**kwargs):
        name=request.data.get('name')
        color=request.data.get('color')
        number_code=request.data.get('number_code')
        category=request.data.get('category')
        q=Q()
        if name:
            q.add(Q(name__contains=name),'AND')
        if color:
            q.add(Q(color__contains=color),'AND')
        if number_code:
            q.add(Q(number_code__contains=number_code),'AND')
        if category:
            q.add(Q(category__id=category),'AND')
        queryset=GoodsModel.objects.filter(q)
        data=GoodsSearchSerializer(instance=queryset,many=True).data
        return Response(data)

