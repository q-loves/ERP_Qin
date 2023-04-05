from django.db.models import Sum
from good_info.models import GoodsModel,GoodsInventoryModel


def get_current_inventory(id):
    cur_inventory=GoodsInventoryModel.objects.filter(goods__id=id).aggregate(sum=Sum('cur_inventory'))
    return cur_inventory['sum']

