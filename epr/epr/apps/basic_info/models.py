from django.db import models

# Create your models here.

from django.db import models


# Create your models here.

# 国家的模型类
from epr.utils.base_model import BaseModel


class Nation(models.Model):
    n_name = models.CharField('国家名称', max_length=30)

    class Meta:
        db_table = 'nation'
        verbose_name = '国家表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.n_name


# 省份的模型类
class Province(models.Model):
    p_name = models.CharField('省份名称', max_length=30)
    nation = models.ForeignKey('Nation', related_name='province_list', on_delete=models.CASCADE, verbose_name='省份所在的国家')

    class Meta:
        db_table = 'province'
        verbose_name = '省份表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.p_name


# 城市的模型类
class City(models.Model):
    c_name = models.CharField('城市名称', max_length=30)
    province = models.ForeignKey('Province', related_name='city_list', on_delete=models.CASCADE, verbose_name='城市所在的省份')

    class Meta:
        db_table = 'city'
        verbose_name = '城市表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.c_name

# 供应商模型类
class SupplierModel(BaseModel):
    name = models.CharField(max_length=100, verbose_name='供应商名称', unique=True,blank=True,null=True)
    mobile = models.CharField('手机号码', max_length=11,blank=True,null=True)
    phone = models.CharField('联系电话', max_length=22,blank=True,null=True)
    contacts_name = models.CharField('联系人名', max_length=22,blank=True,null=True)
    email = models.CharField('电子邮箱', max_length=50,blank=True,null=True)
    ratepayer_number = models.CharField('纳税人识别号码', max_length=50,blank=True,null=True)
    bank = models.CharField('开户银行', max_length=50,blank=True,null=True)
    account_number = models.CharField('银行账号', max_length=50,blank=True,null=True)
    nation = models.CharField('国家', max_length=50,blank=True,null=True)
    province = models.CharField('省份', max_length=50,blank=True,null=True)
    city = models.CharField('城市', max_length=50,blank=True,null=True)
    address = models.CharField('详细地址', max_length=50,blank=True,null=True)
    remark = models.CharField('备注', max_length=512,blank=True,null=True)
    init_pay = models.DecimalField('初期应付', max_digits=20, decimal_places=2,blank=True,null=True)  # 精确到小数点后两位
    current_pay = models.DecimalField('末期应付', max_digits=20, decimal_places=2,blank=True,null=True)  # 精确到小数点后两位
    order_number = models.IntegerField('排序号码', default=100,blank=True,null=True)
    delete_flag=models.CharField('启用or禁用',max_length=1,default='0')

    class Meta:
        db_table = 't_supplier'
        verbose_name = '供应商'
        verbose_name_plural = verbose_name
        ordering = ['order_number', 'id']

    def __str__(self):
        return self.name

# 客户模型类
class CustomerModel(BaseModel):
    name = models.CharField(max_length=100, verbose_name='客户名称', unique=True)
    mobile = models.CharField('手机号码', max_length=11, blank=True, null=True)
    phone = models.CharField('联系电话', max_length=22, blank=True, null=True)
    contacts_name = models.CharField('联系人名', max_length=22, blank=True, null=True)
    email = models.CharField('电子邮箱', max_length=50, blank=True, null=True)
    ratepayer_number = models.CharField('纳税人识别号码', max_length=50, blank=True, null=True)
    bank = models.CharField('开户银行', max_length=50, blank=True, null=True)
    account_number = models.CharField('银行账号', max_length=50, blank=True, null=True)
    nation = models.CharField('国家', max_length=50, blank=True, null=True)
    province = models.CharField('省份', max_length=50, blank=True, null=True)
    city = models.CharField('城市', max_length=50, blank=True, null=True)
    address = models.CharField('详细地址', max_length=50, blank=True, null=True)
    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    init_receivable = models.DecimalField('初期应收', max_digits=20, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    current_receivable = models.DecimalField('末期应收', max_digits=20, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    order_number = models.IntegerField('排序号码', default=100)

    class Meta:
        db_table = 't_customer'
        verbose_name = '客户'
        verbose_name_plural = verbose_name
        ordering = ['order_number', 'id']

    def __str__(self):
        return self.name

# 仓库模型类
class WarehouseModel(BaseModel):
    name = models.CharField(max_length=100, verbose_name='仓库名称', unique=True)
    nation = models.CharField('国家', max_length=50, blank=True, null=True)
    province = models.CharField('省份', max_length=50, blank=True, null=True)
    city = models.CharField('城市', max_length=50, blank=True, null=True)
    address = models.CharField('详细地址', max_length=50, blank=True, null=True)
    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    warehouse_fee = models.DecimalField('仓储费用(元/天/KG)', max_digits=10, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    truckage = models.DecimalField('搬运费用', max_digits=10, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    order_number = models.IntegerField('排序号码', default=100, blank=True, null=True)
    is_default = models.BooleanField('是否默认的仓库', default=False)
    # 用户模型来自于erp_system的APP中，必须要加前缀
    leader_user = models.ForeignKey('erp_system.UserModel', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='仓库负责人')

    class Meta:
        db_table = 't_warehouse'
        verbose_name = '仓库'
        verbose_name_plural = verbose_name
        ordering = ['order_number', 'id']

    def __str__(self):
        return self.name

# 结算账户模型类
class SettlementAccountModel(BaseModel):
    name = models.CharField(max_length=100, verbose_name='仓库名称', unique=True)
    number_code = models.CharField('编号', max_length=28, unique=True)
    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    init_amount = models.DecimalField('初期金额', max_digits=10, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    balance = models.DecimalField('余额', max_digits=10, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    order_number = models.IntegerField('排序号码', default=100)
    is_default = models.BooleanField('是否默认', default=False)

    class Meta:
        db_table = 't_settlement_account'
        verbose_name = '仓库'
        verbose_name_plural = verbose_name
        ordering = ['order_number', 'id']

    def __str__(self):
        return self.name

