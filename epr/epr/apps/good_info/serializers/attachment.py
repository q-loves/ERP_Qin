from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from good_info.models import AttachmentModel


class AttachmentSerializer(ModelSerializer):

    file_name=serializers.CharField(source='a_file.name',read_only=True)
    # file_url=serializers.CharField(source='fdfs_url',read_only=True)
    type_display=serializers.CharField(source='get_a_type_display',read_only=True)

    class Meta:
        model=AttachmentModel
        fields='__all__'
        extra_kwargs={
            'fdfs_url':{
                'read_only':True
            }
        }