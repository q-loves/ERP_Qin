from django.conf import settings
from django.core.files.storage import Storage


class NewFastdfsStorage(Storage):
    def __init__(self):
        self.fdfs_base_url=settings.FDFS_BASE_URL
    def url(self,name):
        return self.fdfs_base_url + name