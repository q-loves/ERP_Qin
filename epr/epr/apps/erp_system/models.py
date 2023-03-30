from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from epr.utils.base_model import BaseModel


class MenuModel(BaseModel):

    number=models.IntegerField(verbose_name='排序数字',blank=True,null=True)
    url=models.CharField(verbose_name='菜单网址',max_length=256,blank=True,null=True)
    name=models.CharField(verbose_name='菜单名字',max_length=256)
    delete_flag=models.CharField(verbose_name='删除标志',max_length=1,default='0')
    parent=models.ForeignKey('self',on_delete=models.CASCADE,related_name='children',blank=True,null=True)

    class Meta:
        db_table='t_menu'
        verbose_name='菜单名称'
        verbose_name_plural=verbose_name

class UserModel(AbstractUser,BaseModel):

    phone=models.CharField(verbose_name='电话号码',max_length=11,blank=True,null=True)
    roles=models.ManyToManyField('RoleModel',blank=True,null=True,db_table='t_user_roles')
    permissions=models.ManyToManyField('PermissionModel',blank=True,null=True,db_table='t_user_permissions')
    dept=models.ForeignKey('DeptModel',verbose_name='部门',related_name='user',blank=True,null=True,on_delete=models.SET_NULL)
    class Meta:
        db_table='t_user'
        verbose_name='用户列表'
        verbose_name_plural=verbose_name

class PermissionModel(BaseModel):
    method_choices=(
        ('POST','增'),('GET','查'),('PUT','改'),('PATCH','局部改'),('DELETE','删')
    )
    name=models.CharField(verbose_name='权限名',max_length=128,blank=True,null=True)
    is_menu=models.BooleanField(verbose_name='是否为菜单',default=True)
    #操作
    method=models.CharField(verbose_name='请求方法',max_length=16,blank=True,null=True,choices=method_choices)
    path=models.CharField(verbose_name='请求路径',max_length=128,blank=True,null=True)
    #资源
    menu=models.ForeignKey('MenuModel',blank=True,null=True,related_name='permission',on_delete=models.CASCADE)
    desc=models.CharField(verbose_name='权限描述',blank=True,null=True,max_length=512)
    class Meta:
        db_table='t_permissions'
        verbose_name='权限列表'
        verbose_name_plural=verbose_name

class RoleModel(BaseModel):
    name=models.CharField(verbose_name='角色名',blank=True,null=True,max_length=32)
    permission=models.ManyToManyField('PermissionModel',blank=True,null=True,db_table='t_role_permission')
    class Meta:
        db_table='t_role'
        verbose_name='角色名称'
        verbose_name_plural=verbose_name

class DeptModel(BaseModel):
    name=models.CharField(verbose_name='部门名称',max_length=16,unique=True)
    address=models.CharField(verbose_name='部门地址',max_length=16,blank=True,null=True)
    parent=models.ForeignKey('self',verbose_name='父部门',related_name='children',blank=True,null=True,on_delete=models.CASCADE)

    class Meta:
        db_table='t_dept'
        verbose_name='部门列表'
        verbose_name_plural=verbose_name


