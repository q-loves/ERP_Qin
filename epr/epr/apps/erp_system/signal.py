# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from erp_system.models import MenuModel,PermissionModel
# from rest_framework import status
# from rest_framework.response import Response
#
# methods={'POST':'新增','GET':'查询','DELETE':'删除','PUT':'修改','PATCH':'局部修改'}
#
# @receiver(post_save,sender=MenuModel)
# def create_menus_permissions(sender,instance,created,**kwargs):
#     if created:
#         if isinstance(instance,MenuModel):
#             #判断是否为父菜单
#             if not instance.parent:
#                 permission=PermissionModel.objects.create(
#                     name=instance.name+'的权限',
#                     is_menu=True,
#                     menu=instance
#                 )
#                 # permission.menu=instance
#                 # permission.save()
#             else:
#                 for method in methods.keys():
#                     permission=PermissionModel.objects.create(
#                         name=instance.name+methods.get(method)+'的权限',
#                         is_menu=False,
#                         method=method,
#                         path=instance.url
#                     )
#                     permission.menu=instance
#                     permission.save()
#         else :
#             return Response(data={'message':'传入的类型不正确'},status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(data={'message': '传入的类型不正确'}, status=status.HTTP_400_BAD_REQUEST)





