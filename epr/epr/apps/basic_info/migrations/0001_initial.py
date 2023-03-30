# Generated by Django 3.2.15 on 2023-03-23 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_name', models.CharField(max_length=30, verbose_name='国家名称')),
            ],
            options={
                'verbose_name': '国家表',
                'verbose_name_plural': '国家表',
                'db_table': 'nation',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=30, verbose_name='省份名称')),
                ('nation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='province_list', to='basic_info.nation', verbose_name='省份所在的国家')),
            ],
            options={
                'verbose_name': '省份表',
                'verbose_name_plural': '省份表',
                'db_table': 'province',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=30, verbose_name='城市名称')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_list', to='basic_info.province', verbose_name='城市所在的省份')),
            ],
            options={
                'verbose_name': '城市表',
                'verbose_name_plural': '城市表',
                'db_table': 'city',
                'ordering': ['id'],
            },
        ),
    ]
