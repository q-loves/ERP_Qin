from rest_framework.viewsets import ModelViewSet

from basic_info.models import CustomerModel

from basic_info.serializers.customer import CustomerSerializer

from epr.utils.base_views.get_queryset_by_keywords import GetQuerysetByKeywords


class CustomerView(ModelViewSet,GetQuerysetByKeywords):

    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer

    # keywords=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
    #     'name':openapi.Schema(type=openapi.TYPE_STRING),
    #     'phone':openapi.Schema(type=openapi.TYPE_STRING)
    # })
    # @swagger_auto_schema(methods=['post'],request_body=keywords,operation_description='输入关键词查询')
    # @action(methods=['post'],detail=False)
    # def get_customer_by_keywords(self,request,*args,**kwargs):
    #     name=request.data.get('name')
    #     phone=request.data.get('phone')
    #     query= Q()
    #     if name:
    #         query.add(Q(name__contains=name),'AND')
    #     if phone:
    #         query.add(Q(phone__contains=phone),'AND')
    #     queryset=CustomerModel.objects.filter(query).all()
    #     data=CustomerSerializer(instance=queryset,many=True).data
    #     return Response(data)
