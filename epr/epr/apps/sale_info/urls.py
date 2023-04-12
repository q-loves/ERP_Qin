from rest_framework.routers import SimpleRouter

from sale_info.views.sale import SaleView

urlpatterns=[

]

router=SimpleRouter()
router.register('sale',SaleView)

urlpatterns+=router.urls