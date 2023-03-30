# Generated by Django 3.2.15 on 2023-03-28 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('good_info', '0002_unitsmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('a_file', models.FileField(upload_to='', verbose_name='文件路径')),
                ('a_type', models.CharField(blank=True, choices=[('image', '图片'), ('doc', 'word文档'), ('excel', 'excel文档'), ('zip', '压缩文件'), ('other', '其他文件')], max_length=20, null=True, verbose_name='文件类型')),
            ],
            options={
                'verbose_name': '附加文件',
                'verbose_name_plural': '附加文件',
                'db_table': 't_attachment',
            },
        ),
    ]