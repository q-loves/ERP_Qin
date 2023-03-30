from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from erp_system.serializers.permission import PermissionSerializer

from erp_system.models import PermissionModel, MenuModel

from erp_system.models import RoleModel
from epr.utils.multiple_delete import MultipleDeleteMixin


class PermissionView(ModelViewSet,MultipleDeleteMixin):
    serializer_class = PermissionSerializer
    queryset = PermissionModel.objects.all()
    #查询菜单权限
    param0 = openapi.Parameter(name='rid', in_=openapi.IN_QUERY, description='查询权限', type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(methods=['GET'], manual_parameters=[param0])
    @action(methods=['get'],detail=False)
    def get_permission_by_menu(self,request,*args,**kwargs):
        menu_id=request.query_params.get('id')
        permissions=PermissionModel.objects.filter(menu__id=menu_id).all()
        ser=PermissionSerializer(instance=permissions,many=True)
        return Response(ser.data)

    param=openapi.Parameter(name='rid',in_=openapi.IN_QUERY,description='查询权限',type=openapi.TYPE_INTEGER)

    #查询树形权限
    @swagger_auto_schema(methods=['GET'],manual_parameters=[param])
    @action(methods=['GET'],detail=False)
    def get_permission(self, request, *args, **kwargs):
        result={}#用于存放最后返回结果
        tree_dict={}
        data=[]
        rid=request.query_params.get('rid')
        #查询当前用户所有已经授权的permission_id
        ids=RoleModel.objects.filter(id=rid).values_list('permission',flat=True).distinct()
        result['ids']=ids
        permissions=PermissionModel.objects.values('id','name','menu__id','menu__name','menu__parent__id')
        #建造一级树,将所有permission放进一个字典中
        for permission in permissions:
            tree_dict[permission['name']]=permission
            # print('permission-------------->',permission)
        #将父节点与子节点分开
        for i in tree_dict:
            if tree_dict[i]['menu__parent__id']:#如果有父菜单
                pid=tree_dict[i]['menu__parent__id']
                permission=PermissionModel.objects.get(menu_id=pid)
                permission_name=PermissionSerializer(instance=permission,many=False).data['name']

                parent=tree_dict[permission_name]
                child=dict()
                child['menu_id']=tree_dict[i]['menu__id']
                child.setdefault('permissions', [])
                parent.setdefault('children',[]).append(child)
            else:#如果无父菜单
                data.append(tree_dict[i])


        #将子权限放入子节点中
        for parent in data:
            if 'children' in parent:
                for child in parent['children']:
                    for permission in permissions:
                        if permission['menu__parent__id'] and permission['menu__id']== child['menu_id']:
                            child['permissions'].append(permission)


        result['data']=data
        return Response(result)










    # #批量删除
    # def multiple_delete(self,request,*args,**kwargs):
    #     del_ids=request.data.get('ids')
    #     if not del_ids:
    #         return Response(data={'message':'请传入数据'},status=status.HTTP_400_BAD_REQUEST)
    #     if not isinstance(del_ids,list):
    #         return Response(data={'message':'请选择至少两个数据'},status=status.HTTP_400_BAD_REQUEST)
    #     permission_del=PermissionModel.objects.filter(id__in=del_ids)
    #     if len(del_ids)!=permission_del.count():
    #         return Response(data={'message':'您要删除的数据不存在！'},status=status.HTTP_400_BAD_REQUEST)
    #     permission_del.update(delete_flag='1')
    #     return Response(data={'message':'删除成功'},status=status.HTTP_204_NO_CONTENT)


