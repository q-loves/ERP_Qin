import json
import re

from django.conf import settings
from django_redis import get_redis_connection
from rest_framework.permissions import BasePermission

from erp.utils.cache_permissions import cache_user_permissions


class RbacPermission(BasePermission):
    def do_url(self,url):
        uri='/api/'+url+'/'
        return re.sub(r'/+',r'/',uri)


    def has_permission(self, request, view):
        """
        1.判断是否为白名单里面的路径，或是admin，直接放行
        2.从redis中取出用户权限
        3.根据url判断用户是否有权限访问
        """
        request_url=request.path
        request_method=request.method

        for item in settings.WHITE_LIST:
            if re.match(settings.REGEX_URL.format(url=item),request_url):
                return True
        roles=request.user.roles.values_list('name',flat=True)
        if 'admin' in roles:
            return True
        #把权限提取出来
        redis_conn=get_redis_connection("default")
        if not redis_conn.exists(f'user_{request.user.id}'):
            cache_user_permissions(request.user)#做安全保护，防止登陆时权限未保存到Redis中
        urls=redis_conn.hkeys(f'user_{request.user.id}')
        #校验路径是否匹配
        redis_key=None
        for url in urls:
           if re.match(settings.REGEX_URL.format(url=self.do_url(url.decode())),request_url) :
               redis_key=url.decode()

               break
        else:
             return False
        #校验请求方法是否匹配
        permissions=json.loads(redis_conn.hget(f'user_{request.user.id}',redis_key).decode())

        for permission in permissions:

            if permission.get('method')==request_method:

                return True


        return False



