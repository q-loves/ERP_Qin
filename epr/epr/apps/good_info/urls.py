from rest_framework.routers import SimpleRouter

from good_info.views.goodscategory import GoodsCategoryView

from good_info.views.units import UnitsView

from good_info.views.attachment import AttachmentView

from good_info.views.goods import GoodsView

urlpatterns=[

]
router=SimpleRouter()
router.register('goodscategory',GoodsCategoryView)
router.register('units',UnitsView)
router.register('attachment',AttachmentView)
router.register('goods',GoodsView)

urlpatterns+=router.urls