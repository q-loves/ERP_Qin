from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from basic_info.serializers.supplier import SupplierSerializer

from basic_info.models import SupplierModel

from epr.utils.base_views.get_queryset_by_keywords import GetQuerysetByKeywords
from epr.utils.base_views.multiple_open import MultipleOpenOrClose


class SupplierView(ModelViewSet,MultipleOpenOrClose,GetQuerysetByKeywords):

    queryset = SupplierModel.objects.all()
    serializer_class = SupplierSerializer

    keywords=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
        'name':openapi.Schema(type=openapi.TYPE_STRING),
        'mobile':openapi.Schema(type=openapi.TYPE_STRING),
        'city':openapi.Schema(type=openapi.TYPE_STRING)

    })
    @swagger_auto_schema(methods=['post'],operation_description='传入关键词，来查询内容',request_body=keywords)
    @action(methods=['post'],detail=False)
    def get_value_by_key(self,request):
        name=request.data.get('name')
        mobile=request.data.get('mobile')
        city=request.data.get('city')
        q=Q()
        if name:
            q.add(Q(name__contains=name),'AND')
        if mobile:
            q.add(Q(mobile__contains=mobile),'AND')
        if city:
            q.add(Q(city__contains=city),'AND')
        supplier=SupplierModel.objects.filter(q).all()
        data=SupplierSerializer(instance=supplier,many=True).data
        return Response(data)




