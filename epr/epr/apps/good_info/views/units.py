from rest_framework.viewsets import ModelViewSet

from good_info.models import UnitsModel

from good_info.serializers.units import UnitsSerializer


class UnitsView(ModelViewSet):

    queryset = UnitsModel.objects.all()
    serializer_class = UnitsSerializer

