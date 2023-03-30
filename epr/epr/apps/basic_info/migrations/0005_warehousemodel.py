# Generated by Django 3.2.15 on 2023-03-27 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basic_info', '0004_customermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='仓库名称')),
                ('nation', models.CharField(blank=True, max_length=50, null=True, verbose_name='国家')),
                ('province', models.CharField(blank=True, max_length=50, null=True, verbose_name='省份')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='城市')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='详细地址')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
                ('warehouse_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='仓储费用(元/天/KG)')),
                ('truckage', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='搬运费用')),
                ('order_number', models.IntegerField(blank=True, default=100, null=True, verbose_name='排序号码')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否默认的仓库')),
                ('leader_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='仓库负责人')),
            ],
            options={
                'verbose_name': '仓库',
                'verbose_name_plural': '仓库',
                'db_table': 't_warehouse',
                'ordering': ['order_number', 'id'],
            },
        ),
    ]