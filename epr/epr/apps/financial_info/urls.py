from rest_framework.routers import SimpleRouter

from financial_info.views.payment import PaymentView

urlpatterns=[

]

router=SimpleRouter()
router.register('payment',PaymentView)

urlpatterns+=router.urls
