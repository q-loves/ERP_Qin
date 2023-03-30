from rest_framework.viewsets import ModelViewSet

from good_info.models import GoodsCategoryModel

from good_info.serializers.goodscategory import GoodsCategorySerializer


class GoodsCategoryView(ModelViewSet):

    queryset = GoodsCategoryModel.objects.filter(parent__isnull=True).all()
    serializer_class = GoodsCategorySerializer

