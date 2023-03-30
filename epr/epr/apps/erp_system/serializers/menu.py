from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from erp_system.models import MenuModel


class MenuSerializer(ModelSerializer):

    children=serializers.SerializerMethodField(read_only=True)


    class Meta:
        model=MenuModel
        fields='__all__'

    def get_children(self,obj):
        if obj.children:
            return MenuSerializer(instance=obj.children,many=True).data


