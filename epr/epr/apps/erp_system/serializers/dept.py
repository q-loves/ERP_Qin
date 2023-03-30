from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from erp_system.models import DeptModel

# class ChildSerializer(ModelSerializer):
#
#     children=serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model=DeptModel
#         fields=['id','name','parent','children']
#
#     def get_children(self,obj):
#         print('obj------->',obj)
#         if obj.children:
#             return ChildSerializer(instance=obj.children,many=True).data
#
#         return None



class DeptSerializer(ModelSerializer):

    # children=ChildSerializer(read_only=True,many=True)
    children=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=DeptModel
        fields='__all__'

    def get_children(self,obj):
        if obj.children:
            return DeptSerializer(instance=obj.children,many=True).data
        return None