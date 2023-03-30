import random
import string
import time
from enum import Enum, unique

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


def generate_code(prefix):
    """
    生成随机编号，3位prefix，14位日期，7位微妙，4位随机数

    """
    num=string.digits
    random_num=random.choices(num,k=4)
    random_num=''.join(random_num)
    code=f'{prefix}{time.strftime("%Y%m%d%H%M%S",time.localtime())}{str(time.time()).replace(".","")[-7:]}{random_num}'
    return code

@unique
class Perfix(Enum):
    #结账编号前缀
    acc='ACC'
    #订单
    ord='ORD'
    #商品类别
    cat='CAT'
    #商品信息
    goo='GOO'

class GenerateCodeView(APIView):
    param=openapi.Parameter(type=openapi.TYPE_STRING,name='prefix',in_=openapi.IN_QUERY,description='传入prefix')
    @swagger_auto_schema(manual_parameters=[param],operation_description='传入prefix')
    @action(methods=['get'],detail=False)
    def get(self,request,*args,**kwargs):
        prefix=request.query_params.get('prefix')
        if prefix:
            if prefix in Perfix.__members__:
                code=generate_code(Perfix[prefix].value)
                return Response(data={'code':code})
            return Response(data={'message':'prefix有误，请重新输入'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'message':'prefix为必传参数'},status=status.HTTP_400_BAD_REQUEST)
