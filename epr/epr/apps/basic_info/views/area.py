from django.shortcuts import render

# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from basic_info.models import Nation, Province, City
from basic_info.serializers.area import NationSerializer,ProvinceSerializer,CitySerializer




class NationView(ModelViewSet):

    queryset = Nation.objects.all()
    serializer_class = NationSerializer




class ProvinceView(ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

    param = openapi.Parameter(name='nid', in_=openapi.IN_QUERY, description='查询权限', type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(methods=['GET'], manual_parameters=[param])
    @action(methods=['get'],detail=False)
    def get_province_by_nation(self,request):
        nid = self.request.query_params.get('nid')
        if nid:
            nid = int(nid)
            province= Province.objects.filter(nation_id=nid).all()
        else:
            province= Province.objects.all()
        data=ProvinceSerializer(instance=province,many=True).data
        return Response(data)

class CityView(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    param = openapi.Parameter(name='pid', in_=openapi.IN_QUERY, description='查询权限', type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(methods=['GET'], manual_parameters=[param])
    @action(methods=['get'], detail=False)
    def get_city_by_province(self,request):
        pid = request.query_params.get('pid')
        if pid:
            nid = int(pid)
            city= City.objects.filter(province_id=pid).all()
        else:
            city= City.objects.all()
        data=CitySerializer(instance=city,many=True).data
        return Response(data)