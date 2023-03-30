from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from erp_system.models import DeptModel

from erp_system.serializers.dept import DeptSerializer

# param = openapi.Parameter(name='pid', in_=openapi.IN_QUERY, description='查询权限', type=openapi.TYPE_INTEGER)
# @method_decorator(name='list',decorator=swagger_auto_schema( manual_parameters=[param]))
class DeptView(ModelViewSet):

    queryset = DeptModel.objects.filter(parent__isnull=True).all()
    serializer_class = DeptSerializer

    param = openapi.Parameter(name='pid', in_=openapi.IN_QUERY, description='查询权限', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(methods=['GET'], manual_parameters=[param])
    @action(methods=['get'], detail=False)
    def get_dept(self,request):
        pid=request.query_params.get('pid',None)
        if pid:
            if int(pid)==0:
                dept= DeptModel.objects.filter(parent__isnull=True).all()
            else:
                dept= DeptModel.objects.filter(Q(id=pid)).all()
        else:
            dept= DeptModel.objects.filter(parent__isnull=True).all()

        data=DeptSerializer(instance=dept,many=True).data
        return Response(data)


