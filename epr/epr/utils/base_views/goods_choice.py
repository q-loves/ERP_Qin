from django.db.models import Q, Sum, Subquery, OuterRef
from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import GenericAPIView

from good_info.models import GoodsModel,GoodsInventoryModel
from rest_framework.response import Response

from epr.utils.base_serializers import GoodsChoiceSerializer


class GoodsChoiceView(GenericAPIView):

    serializer_class = GoodsChoiceSerializer

    @swagger_auto_schema(operation_description='传入关键词查询',request_body=GoodsChoiceSerializer)
    def post(self,request,*args,**kwargs):
        ser=GoodsChoiceSerializer(data=request.data)
        if ser.is_valid():#校验传入关键词是否符合规格
            keywords=ser.validated_data.get('keywords',None)
            warehouse_id=ser.validated_data.get('warehouse_id',None)
            category_id=ser.validated_data.get('category_id',None)
            number_code=ser.validated_data.get('number_code',None)
            q=Q()
            #先把每个商品的库存算出来
            if warehouse_id:
                inventory=GoodsInventoryModel.objects.filter(warehouse_id=warehouse_id).filter(goods_id=OuterRef('pk')).values('goods_id').annotate(total_inventory=Sum('cur_inventory'))
            else:
                inventory=GoodsInventoryModel.objects.filter(goods_id=OuterRef('id')).values('goods_id').annotate(total_inventory=Sum('cur_inventory'))

            #开始根据关键词查询
            if keywords:
                q.add(Q(name__contains=keywords),'AND')
            if number_code:
                q.add(Q(number_code__contains=number_code),'AND')
            if category_id:
                q.add(Q(category_id=category_id),'AND')
            #把两次查询的结果追加到一起
            data=GoodsModel.objects.filter(q).values('id','name','specification','model_number','color','units__basic_name','category__name').annotate(cur_inventory=Subquery(inventory.values('total_inventory'))).all()

            return Response(data=data)




