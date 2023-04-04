from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from basic_info.models import WarehouseModel

from basic_info.serializers.warehouse import WarehouseSearchSerializer,WarehouseSimpleSerializer

from epr.tasks import create_warehouse_inventory
from epr.utils.base_views.get_queryset_by_keywords import GetQuerysetByKeywords


class WarehouseView(ModelViewSet,GetQuerysetByKeywords):

    queryset = WarehouseModel.objects.all()

    def get_serializer_class(self):
        if self.action=='list' or self.action=='get_queryset_by_keywords':
            return WarehouseSearchSerializer
        else:
            return WarehouseSimpleSerializer

    #重写create，来调用celery中的task
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        warehouse=serializer.save()
        create_warehouse_inventory.delay(warehouse.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


