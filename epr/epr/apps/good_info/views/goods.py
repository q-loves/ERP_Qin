from rest_framework.viewsets import ModelViewSet

from good_info.models import GoodsModel

from good_info.serializers.goods import GoodsSimpleSerializer


class GoodsView(ModelViewSet):

    queryset = GoodsModel.objects.all()
    serializer_class = GoodsSimpleSerializer

