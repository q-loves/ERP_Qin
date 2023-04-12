from rest_framework.viewsets import ModelViewSet

from sale_info.models import SaleModel

from sale_info.serializers.sale import SaleSerializer,SaleSearchSerializer

from epr.utils.base_views.multiple_audit import MultipleAuditMixin
from epr.utils.base_views.multiple_delete import MultipleDeleteMixin


class SaleView(ModelViewSet,MultipleDeleteMixin,MultipleAuditMixin):

    queryset = SaleModel.objects.all()

    def get_serializer_class(self):
        if self.action=='retrieve':
            return SaleSearchSerializer
        return SaleSerializer
