from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, GenericAPIView

from erp_system.serializers.user import UserSerializer

from erp_system.models import UserModel
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from erp_system.serializers.user import UpdateOrDeleteSerializer

from erp_system.serializers.user import ListOrRetrieveSerializer

from erp_system.serializers.user import ResetPasswordSerializer
from erp.utils.multiple_delete import MultipleDeleteMixin

class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.order_by('id')

#除了注册和修改密码外的所有功能
class UserView(mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               MultipleDeleteMixin,
               GenericViewSet):

    queryset = UserModel.objects.all()
    serializer_class = UpdateOrDeleteSerializer

    def get_serializer_class(self):
        if self.action=='update' or self.action=='partial_update' or self.action=='destroy':
            return UpdateOrDeleteSerializer
        else:
            return ListOrRetrieveSerializer

class ResetPasswordView(mixins.UpdateModelMixin,
                        GenericAPIView):

    queryset = UserModel.objects.all()
    serializer_class = ResetPasswordSerializer

    # def patch(self,request,*args,**kwargs):
    #     return self.partial_update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        username=self.request.data.get('username')
        password=request.data.get('password')
        new_password=request.data.get('new_password')
        user=UserModel.objects.get(username=username)
        if not user:
            return Response(data={'message':f'没有用户名为{username}的用户'})
        if not user.check_password(password):
            return Response(data={'message':'原密码错误'},status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()

        return Response(data={'message':'修改成功'})












