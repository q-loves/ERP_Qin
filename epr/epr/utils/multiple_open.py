from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class MultipleOpenOrClose():
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'is_open': openapi.Schema(type=openapi.TYPE_STRING),
        'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER))
    })

    @swagger_auto_schema(methods=['delete'], request_body=request_body, operation_description='批量删除或增加')
    @action(methods=['delete'], detail=False)
    def multiple_open_or_close(self,request,*args,**kwargs):
        is_open=request.data.get('is_open')
        ids=request.data.get('ids')
        if not all([is_open,ids]):
            return Response(data={'message':'缺少必传参数'},status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(ids,list):
            return Response(data={'message':'传入参数形式不正确'},status=status.HTTP_400_BAD_REQUEST)
        query=self.get_queryset()
        oc_query=query.filter(id__in=ids)
        if len(ids)!=oc_query.count():
            return Response(data={'message':'要删除的数据不存在'},status=status.HTTP_400_BAD_REQUEST)
        oc_query.update(delete_flag=is_open)
        return Response(data={'message':'操作成功'},status=status.HTTP_200_OK)


