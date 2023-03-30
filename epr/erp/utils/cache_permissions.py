import json

from django.db.models import Q
from django_redis import get_redis_connection
from erp_system.models import PermissionModel


def cache_user_permissions(user):
    #提取出该用户的所有权限
    permission_id=user.roles.values_list('permission',flat=True).distinct()
    permission_id2=user.permissions.values_list('id',flat=True).distinct()
    #根据权限id获取权限的具体信息
    #is_menu=False,排除父菜单，因为获得GET权限时就可判断书否有父菜单的权限
    permissions=PermissionModel.objects.filter(Q(is_menu=False)&(Q(id__in=permission_id)|Q(id__in=permission_id2))).values('id','name','method','path')
    permission_dict={}

    for permission in permissions:
        #因为要转换成json格式，所以要去除不可见符号
        path=str(permission.get('path')).replace('\u200b','')
        method=str(permission.get('method')).replace('\u200b','')
        _name=str(permission.get('name')).replace('\u200b','')
        _id=str(permission.get('id')).replace('\u200b','')

        if permission_dict.get(path):
            permission_dict[path].append({
                'method':method,
                '_name':_name,
                '_id':_id
            })
        else:
            permission_dict[path]=[{
                'method': method,
                '_name': _name,
                '_id': _id
            }]

    for key in permission_dict:
        #将数据转化成json格式
        permission_dict[key]=json.dumps(permission_dict[key])


    redis_conn=get_redis_connection('default')
    redis_conn.hmset(f'user_{user.id}',permission_dict)


