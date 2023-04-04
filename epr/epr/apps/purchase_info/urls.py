from rest_framework.routers import SimpleRouter

from purchase_info.views.purchase import PurchaseView

urlpatterns=[

]
router=SimpleRouter()
router.register('purchase',PurchaseView)

urlpatterns+=router.urls