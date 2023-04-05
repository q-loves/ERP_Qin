from rest_framework.routers import SimpleRouter



from warehouse_info.views.instorage import InStorageView

urlpatterns=[

]

router=SimpleRouter()





router.register('instorage',InStorageView)

urlpatterns+=router.urls