from django.contrib.auth.backends import ModelBackend

from erp_system.models import UserModel

from erp.utils.cache_permissions import cache_user_permissions


class UserLoginAuth(ModelBackend):

    def authenticate(self,request,username=None,password=None,**kwargs):
        try:
            user=UserModel.objects.get(username=username)
        except:
            return None
        if user.check_password(password):
            cache_user_permissions(user)
            return user