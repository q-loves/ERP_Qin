from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class MultipleDeleteMixin():
    delete_ids=openapi.Schema(type=openapi.TYPE_OBJECT,required=['ids'],properties={
        'ids':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER))
    })
    @swagger_auto_schema(method='delete',request_body=delete_ids,operation_description='批量删除')
    @action(methods=['delete'],detail=False)
    def multiple_delete(self,request,*args,**kwargs):
        del_ids=request.data.get('ids')
        if not del_ids:
            return Response(data={"message":'请输入数据'},status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(del_ids,list):
            return Response(data={'message':'传输的数据类型不对'},status=status.HTTP_400_BAD_REQUEST)
        queryset=self.get_queryset()
        del_queryset=queryset.filter(id__in=del_ids)
        if len(del_ids)!=del_queryset.count():
            return Response(data={'message':'数据不存在'},status=status.HTTP_400_BAD_REQUEST)
        del_queryset.delete()
        return Response(data={'message':'删除成功'},status=status.HTTP_204_NO_CONTENT)