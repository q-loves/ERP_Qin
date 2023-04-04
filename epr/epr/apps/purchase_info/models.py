from django.db import models

# Create your models here.
# 采购单 模型类
from epr.utils.base_model import BaseModel


class PurchaseModel(BaseModel):
    invoices_date = models.DateTimeField('单据日期')
    number_code = models.CharField('单据编号,不让用户填写', max_length=28)
    discount = models.DecimalField('优惠率,最多精确到小数点后两位', max_digits=5, decimal_places=2, blank=True, null=True)
    discount_money = models.DecimalField('优惠金额(付款优惠),最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True,
                                         null=True)
    last_amount = models.DecimalField('优惠后总金额,最多精确到小数点后两位', max_digits=13, decimal_places=2, blank=True, null=True)
    deposit = models.DecimalField('支付定金,最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True, null=True)

    number_count = models.DecimalField('采购数量,最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField('状态,0:未审核,1:已审核,2:部分入库,3:全部入库,4:完成采购,5:已付定金', max_length=1, default='0')

    operator_user = models.ForeignKey('erp_system.UserModel', related_name='operator_purchase_list', null=True,
                                      blank=True, on_delete=models.SET_NULL,
                                      verbose_name='采购操作人员，不能修改')

    # 增加一个冗余字段
    operator_user_name = models.CharField('操作人员的真实姓名', max_length=20, null=True, blank=True)
    check_user = models.ForeignKey('erp_system.UserModel', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='审核人员，不能修改')
    # 增加一个冗余字段
    check_user_name = models.CharField('操作人员的真实姓名', max_length=20, null=True, blank=True)

    account = models.ForeignKey('basic_info.SettlementAccountModel', null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name='结算账户，审核之后不能改')

    supplier = models.ForeignKey('basic_info.SupplierModel', null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='供应商，审核之后不能改')
    # 增加一个冗余字段
    supplier_name = models.CharField('供应商名称', max_length=30, null=True, blank=True)

    attachment_list = models.CharField('附件的id列表，字段的值为: 1,2,3,4', max_length=20, null=True, blank=True)

    class Meta:
        db_table = 't_purchase'
        verbose_name = '采购表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
# 采购单中的货品（采购项） 模型类
class PurchaseItemModel(BaseModel):
    #  前三个都是冗余字段，目的在于减少级联查询，减小数据库压力
    name = models.CharField(max_length=20, verbose_name='货品名称')
    specification = models.CharField('货品规格', max_length=50, null=True, blank=True)
    number_code = models.CharField('货品的编号或者批号', max_length=28, null=True, blank=True)

    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    purchase_count = models.DecimalField('采购数量,最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True, null=True)
    purchase_price = models.DecimalField('采购单价,最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True, null=True)
    purchase_money = models.DecimalField('采购金额,最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True, null=True)

    purchase = models.ForeignKey('PurchaseModel', related_name='item_list', null=True, blank=True,
                                 on_delete=models.CASCADE,
                                 verbose_name='采购单')
    goods = models.ForeignKey('good_info.GoodsModel', null=True, blank=True, on_delete=models.SET_NULL,
                              verbose_name='货品')

    class Meta:
        db_table = 't_purchase_items'
        verbose_name = '采购项表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name + ' ' + self.specification

