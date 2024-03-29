# Generated by Django 3.2.15 on 2023-03-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('good_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('basic_name', models.CharField(max_length=20, unique=True, verbose_name='基本单位')),
                ('backup_name', models.CharField(max_length=20, verbose_name='副单位')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '计量单位',
                'verbose_name_plural': '计量单位',
                'db_table': 't_units',
                'ordering': ['id'],
            },
        ),
    ]
