from django.urls import re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from .views.dept import DeptView
from .views.menu import MenuView
from .views.permission import PermissionView
from .views.role import RoleView
from .views.user import RegisterView, UserView, ResetPasswordView

urlpatterns =[
    re_path('user/login/', obtain_jwt_token),
    re_path('^user/register/$',RegisterView.as_view()),
    re_path('^user/reset_password/$',ResetPasswordView.as_view()),
]

router=DefaultRouter()
router.register('menu',MenuView)
router.register('permission',PermissionView)
router.register('role',RoleView)
router.register('user',UserView)
router.register('dept',DeptView)
urlpatterns += router.urls