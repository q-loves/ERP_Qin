from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from basic_info.serializers.customer import CustomerSerializer

from basic_info.serializers.supplier import SupplierSerializer


class GetQuerysetByKeywords():
    keywords=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
        'name':openapi.Schema(type=openapi.TYPE_STRING),
        'phone':openapi.Schema(type=openapi.TYPE_STRING),
    })
    @swagger_auto_schema(methods=['post'],operation_description='传入关键词，来查询内容',request_body=keywords)
    @action(methods=['post'],detail=False)
    def get_queryset_by_keywords(self,request,*args,**kwargs):
        name=request.data.get('name')
        phone=request.data.get('phone')
        city=request.data.get('city')
        q=Q()
        if name:
            q.add(Q(name__contains=name),'AND')
        if phone:
            q.add(Q(phone__contains=phone),'AND')
        if city:
            q.add(Q(city__contains=city),'AND')
        queryset=self.get_queryset()
        pur_queryset=queryset.filter(q).all()
        serializer=self.get_serializer_class()

        data=serializer(instance=pur_queryset,many=True).data
        return Response(data)
