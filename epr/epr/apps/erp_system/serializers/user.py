import re

from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, CharField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from erp_system.models import UserModel

from erp_system.serializers.role import RoleSimpleSerializer

from erp_system.serializers.dept import DeptSerializer

from erp_system.serializers.permission import PermissionSerializer


class UserSerializer(ModelSerializer):

    def validate_phone(self,phone):
        pattern='1[35789]\d{9}'
        if not re.match(pattern,phone):
            raise ValidationError('手机号格式错误')
        return phone
    def create(self, validated_data):
        user=UserModel.objects.create_user(**validated_data)
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return user

    class Meta:
        model = UserModel
        fields = ['username','phone','email','password']
        extra_lwargs={
            'username':{
                'max_length':10,
                'min_length':3
            },
            'password':{
                'max_length':16,
                'min_length':6,
                'write_only':True
            }
        }

class UpdateOrDeleteSerializer(ModelSerializer):

    class Meta:
        model=UserModel
        fields=['id','username','phone','roles','dept','permissions']

class ListOrRetrieveSerializer(ModelSerializer):

    roles=RoleSimpleSerializer(read_only=True,many=True)
    permissions=PermissionSerializer(read_only=True,many=True)
    dept=DeptSerializer(read_only=True,many=False)

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'phone', 'roles', 'dept','permissions']

class ResetPasswordSerializer(ModelSerializer):

    new_password=serializers.CharField(required=True,write_only=True)
    confirm_password=serializers.CharField(required=True,write_only=True)
    class Meta:
        model=UserModel
        fields=['username','password','new_password','confirm_password']
        extra_kwargs={
            'password':{
                'write_only':True
            }
        }

    def validate(self, attrs):
        username=attrs.get('username')
        password=attrs.get('password')
        new_password=attrs.get('new_password')
        confirm_password=attrs.get('confirm_password')
        if not all [username,password,new_password,confirm_password]:
            return Response(data={'message:缺少必传参数'},status=status.HTTP_400_BAD_REQUEST)
        if new_password!=confirm_password:
            return Response(data={'message':'新设置密码输入不正确'},status=status.HTTP_400_BAD_REQUEST)
        return attrs

    # def save(self, **kwargs):
    #     if not self.instance.check_password(self.validated_data.get('password')):
    #         raise ValidationError('原始密码错误')
    #     self.instance.set_password(self.validated_data.get('new_password'))
    #     self.instance.save()
    #     return self.instance





