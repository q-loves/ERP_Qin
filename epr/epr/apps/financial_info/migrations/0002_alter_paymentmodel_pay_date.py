# Generated by Django 3.2.15 on 2023-04-07 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial_info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmodel',
            name='pay_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='付款日期'),
        ),
    ]
