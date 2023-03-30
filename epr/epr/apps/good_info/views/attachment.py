from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from fdfs_client.client import get_tracker_conf, Fdfs_client
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from good_info.models import AttachmentModel

from good_info.serializers.attachment import AttachmentSerializer


class AttachmentView(ModelViewSet):

    queryset = AttachmentModel.objects.all()
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser,)
    file = openapi.Parameter(name='a_file', in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True, description='上传文件')
    @swagger_auto_schema(manual_parameters=[file])
    def create(self, request, *args, **kwargs):

        a_type=request.data.get('a_type',None)
        file=request.data.get('a_file')

        tracker_path = get_tracker_conf(settings.FASTDFS_CONFIG_PATH)
        client = Fdfs_client(tracker_path)
        ret = client.upload_by_buffer(request.data['a_file'].read())
        if ret.get('Status') != 'Upload successed.':
            return Response(data={'message':'上传失败'},status=status.HTTP_403_FORBIDDEN)
        fdfs_url = ret.get('Remote file_id').decode('utf-8')
        file = AttachmentModel.objects.create(a_file=fdfs_url,a_type=a_type)
        data=AttachmentSerializer(instance=file).data
        return Response(data)