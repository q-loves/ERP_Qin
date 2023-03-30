from celery import shared_task, Task

from erp_system.models import MenuModel

from erp_system.models import PermissionModel

from erp_system.serializers.menu import MenuSerializer

from basic_info.models import WarehouseModel

from good_info.models import GoodsModel

from good_info.models import GoodsInventoryModel

methods={'POST':'新增','GET':'查询','DELETE':'删除','PUT':'修改','PATCH':'局部修改'}

@shared_task
def create_menu_permissions(menu_id):
        instance=MenuModel.objects.get(id=menu_id)

        # 判断是否为父菜单
        if not instance.parent:
            permission = PermissionModel.objects.create(
                name=instance.name + '的权限',
                is_menu=True,
                menu=instance
            )
            # permission.menu=instance3
            # permission.save()
        else:
            for method in methods.keys():
                permission = PermissionModel.objects.create(
                    name=instance.name + methods.get(method) + '的权限',
                    is_menu=False,
                    method=method,
                    path=instance.url
                )
                permission.menu = instance
                permission.save()
@shared_task()
def create_warehouse_inventory(warehouse_id):
    warehouse=WarehouseModel.objects.get(id=warehouse_id)
    goods_ids=GoodsModel.objects.values_list('id',flat=True)
    obj_list=[]#用于存放对象，最后一次性写入数据库，减小数据库压力
    for good_id in goods_ids:
        obj_list.append(GoodsInventoryModel(goods_id=good_id,warehouse=warehouse,warehouse_name=warehouse.name))
    GoodsInventoryModel.objects.bulk_create(obj_list)

