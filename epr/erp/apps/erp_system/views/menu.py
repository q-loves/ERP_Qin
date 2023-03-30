from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from erp_system.models import MenuModel, PermissionModel
from erp_system.serializers.menu import MenuSerializer

from erp.tasks import create_menu_permissions


class MenuView(ModelViewSet):
    """
    功能介绍：
    1.新增
    2.查询单个菜单功能
    3.查询所有菜单功能
    4.查询父类菜单所有子菜单
    5.删除
    6.批量删除
    7.修改功能菜单
    """
    queryset = MenuModel.objects.filter(parent__isnull=True,delete_flag=0).all()
    serializer_class=MenuSerializer
    #查询功能
    param = openapi.Parameter(name='pid', in_=openapi.IN_QUERY, description='查询权限', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(method='GET', manual_parameters=[param])
    @action(methods=['get'], detail=False)
    def get_menu(self,request):
        pid=request.query_params.get('pid',None)
        if pid :
            pid=int(pid)
            if pid==0:
                #查询顶级父类的子类
                menu= MenuModel.objects.filter(parent__isnull=True,delete_flag=0).all()
            else:
                #查询指定id的子类
                menu= MenuModel.objects.filter(id=pid,delete_flag=0).all()
        else:
            #查询所有菜单
            menu= MenuModel.objects.filter(parent__isnull=True,delete_flag=0).all()
        data=MenuSerializer(instance=menu,many=True).data
        return Response(data)
    #删除单个菜单功能
    def destory(self,request,*args,**kwargs):
        object=self.get_object()
        #删除目标菜单
        object.delete_flag='1'
        id=object.id
        #删除目标菜单的子菜单
        MenuModel.objects.filter(parent__id=id).update(delete_flag='1')
        return Response(status=status.HTTP_204_NO_CONTENT)

    del_ids=openapi.Schema(type=openapi.TYPE_OBJECT,required=['ids'],properties={
        'ids':openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER))
    })

    #删除多个菜单功能
    @swagger_auto_schema(method='delete',request_body=del_ids,operation_description='批量删除')
    @action(methods=['delete'] , detail=False)
    def multiple_delete(self,request,*args,**kwargs):
        object_list=request.data.get('ids')
        if not object_list:
            return Response(data='缺少必传参数',status=status.HTTP_400_BAD_REQUEST)
        elif not isinstance(object_list,list):
            return Response(data='参数形式不正确',status=status.HTTP_400_BAD_REQUEST)
        else:
            #删除目标菜单
            MenuModel.objects.filter(id__in=object_list).update(delete_flag='1')

            #删除目标菜单的子菜单
            for id in object_list:
                MenuModel.objects.filter(parent__id=id).update(delete_flag='1')
            return Response(status=status.HTTP_204_NO_CONTENT)
    #重写create方法，插入celery的task
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu=serializer.save()
        create_menu_permissions.delay(menu.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #查询当前用户拥有哪些菜单的get权限
    @action(methods=['GET'],detail=False)
    def get_get_permission_menus(self,request,*args,**kwargs):
        result={}
        tree_dict={}
        tree_data=[]
        #通过查询用户角色来获得其权限
        permission_id=request.user.roles.values_list('permission',flat=True).distinct()
        #查询拥有get权限的菜单
        menu_id=PermissionModel.objects.filter(id__in=permission_id).filter(Q(method='GET')|Q(is_menu=True)).values_list('menu_id',flat=True)
        menu_list=MenuModel.objects.filter(id__in=menu_id).all()
        menu_data=MenuSerializer(instance=menu_list,many=True).data


        #创建二级树1.将所有数据装进字典中
        for data in menu_data:
            tree_dict[data['id']]=data
        #2.将父节点与子节点分开
        for i in tree_dict:
            if tree_dict[i]['parent']:
                pid=tree_dict[i]['parent']
                parent=tree_dict[pid]
                parent.setdefault('children',[]).append(tree_dict[i])

            else:
                tree_data.append(tree_dict[i])
        result=tree_data
        return Response(result)







