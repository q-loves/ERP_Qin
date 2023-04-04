from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from erp_system.models import RoleModel

from erp_system.serializers.role import RolePartialSerializer, RoleSimpleSerializer, RolesPartialSerializer

from epr.utils.base_views.multiple_delete import MultipleDeleteMixin
from erp_system.models import PermissionModel


class RoleView(ModelViewSet,MultipleDeleteMixin):


    queryset = RoleModel.objects.all()
    # serializer_class = RoleSimpleSerializer
    def get_serializer_class(self):
        if self.action=='set_permissions_to_role':
            return RolePartialSerializer
        if self.action=='partial_update':
            return RolesPartialSerializer
        else:
            return RoleSimpleSerializer

    def destroy(self,request,*args,**kwargs):
        if self.get_object().name=='admin':
            return Response(data={'message':'该用户不可删除'},status=status.HTTP_403_FORBIDDEN)
        else:
            return super(RoleView, self).destory(request,*args,**kwargs)

    @action(methods=['post'],detail=False)
    def set_permissions_to_role(self,request,*args,**kwargs):
        ser=RolePartialSerializer(data=request.data)
        if ser.is_valid():
            role=RoleModel.objects.get(id=ser.validated_data.get('role_id'))
            permission=PermissionModel.objects.get(id=ser.validated_data.get('permission_id'))
            if ser.validated_data.get('is_create'):
                role.permission.add(permission)
                if  permission.menu.parent:#判断该权限所对应的菜单是否有父菜单
                    print('---------------->',permission.menu.parent_id)
                    permission_parent=PermissionModel.objects.get(menu__id=permission.menu.parent_id)
                    role.permission.add(permission_parent)

            else:
                role.permission.remove(permission)

            result=RoleSimpleSerializer(instance=role)
            return Response(data=result.data)


    delete_ids = openapi.Schema(type=openapi.TYPE_OBJECT,required=['ids'],properties={
        'ids':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER))
    })

    @swagger_auto_schema(method='delete',request_body=delete_ids,operation_description='批量删除')
    @action(methods=['delete'],detail=False)
    def multiple_delete(self,request,*args,**kwargs):
        delete_ids=request.data.get('ids')
        admin=RoleModel.objects.get(name='admin')
        if isinstance(delete_ids,list):
            if admin.id in delete_ids:
                return Response(data={'message':'admin角色不能删除'},status=status.HTTP_403_FORBIDDEN)
            else:
                return super(RoleView, self).multiple_delete(request,*args,**kwargs)
        else:
            return Response(data={'message':'请传入正确格式的数据'},status=status.HTTP_400_BAD_REQUEST)







