from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from purchase_info.models import PurchaseModel

from erp_system.models import UserModel


class MultipleAuditMixin():
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,required=['ids','user_id','is_audit'],properties={
        'ids':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER),description='传入要进行审核的订单的id值'),
        'user_id':openapi.Schema(type=openapi.TYPE_INTEGER,description='传入审核用户的id'),
        'is_audit':openapi.Schema(type=openapi.TYPE_INTEGER,description='传入审核状态')

    })
    @swagger_auto_schema(method='put',request_body=request_body,operation_description='传入关键词')
    @action(methods=['put'],detail=False)
    def multiple_audit(self,request,*args,**kwargs):
        ids=request.data.get('ids')
        user_id=request.data.get('user_id')
        is_audit=request.data.get('is_audit')
        if not all([ids,user_id,is_audit]):
            return Response(data={'message':'缺少必传参数'},status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(ids,list):
            return Response(data={'message':'ids格式不正确'},status=status.HTTP_400_BAD_REQUEST)
        queryset=self.get_queryset()
        aud_queryset=queryset.filter(id__in=ids).all()
        if len(ids)!=aud_queryset.count():
            return Response(data={'message':'要审核的表单不存在'},status=status.HTTP_400_BAD_REQUEST)
        for item in aud_queryset:
            if item.status!='1' and is_audit=='0':#1以后的状态不能反审核
                return Response(data={'message':'1以后的状态不能反审核'},status=status.HTTP_400_BAD_REQUEST)
            if item.status!='0' and is_audit=='1':#0以后的状态不能审核
                return Response(data={'message':'0以后的状态不能审核'},status=status.HTTP_400_BAD_REQUEST)
        check_user=UserModel.objects.get(id=user_id)
        aud_queryset.update(check_user=check_user,status=is_audit,check_user_name=check_user.username)
        return Response(data={'message':'修改成功'},status=status.HTTP_200_OK)

