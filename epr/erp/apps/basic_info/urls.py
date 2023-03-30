from rest_framework.routers import SimpleRouter, DefaultRouter

from .views.customer import CustomerView
from .views.settlement_account import SettlementAccountView
from .views.supplier import SupplierView
from .views.area import NationView, ProvinceView, CityView
from .views.warehouse import WarehouseView

urlpatterns=[

]
router=DefaultRouter()
router.register('nation',NationView)
router.register('province',ProvinceView)
router.register('city',CityView)
router.register('supplier',SupplierView)
router.register('customer',CustomerView)
router.register('warehouse',WarehouseView)
router.register('settlementaccount',SettlementAccountView)

urlpatterns+=router.urls