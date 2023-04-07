from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


# 货币种类
from epr.utils.base_model import BaseModel

currency_choices = (
    ('CNY', '人民币'),
    ('USD', '美元'),
    ('EUR', '欧元'),
    ('JPY', '日元'),
    ('HKD', '港币')
)

# 付款类型
pay_choices = (
    ('1', '采购定金'),
    ('2', '采购货款'),
    ('3', '欠款还款'),
    ('4', '其他付款')
)


# 付款单的模型类
class PaymentModel(BaseModel):
    pay_date = models.DateTimeField('付款日期',blank=True,null=True)
    number_code = models.CharField('单据编号,不让用户填写', max_length=28)

    #当pay_category=2时，pay_money字段应该等于所有付款项目的this_money的总和
    pay_money = models.DecimalField('付款金额最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0)

    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    currency = models.CharField('货币种类', max_length=20, null=True, choices=currency_choices, default='CNY')
    pay_category = models.CharField('付款类型', max_length=2, null=True, choices=pay_choices, default='1')
    status = models.CharField('状态,0:未审核,1:已审核', max_length=1, default='0')

    account = models.ForeignKey('basic_info.SettlementAccountModel', null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name='结算账户，审核之后不能改',related_name='payment')
    operator_user = models.ForeignKey('erp_system.UserModel', related_name='operator_pay_list', null=True,
                                      blank=True, on_delete=models.SET_NULL,
                                      verbose_name='财务操作人员，不能修改')
    # 增加一个冗余字段
    operator_user_name = models.CharField('财务人员的真实姓名', max_length=20, null=True, blank=True)
    check_user = models.ForeignKey('erp_system.UserModel', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='审核人员，不能修改')
    # 增加一个冗余字段
    check_user_name = models.CharField('审核人员的真实姓名', max_length=20, null=True, blank=True)

    supplier = models.ForeignKey('basic_info.SupplierModel', null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='供应商，审核之后不能改')
    # 增加一个冗余字段
    supplier_name = models.CharField('供应商名称', max_length=30, null=True, blank=True)
    purchase = models.ForeignKey('purchase_info.PurchaseModel', null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='采购订单，审核之后不能改',related_name='payment')
    attachment_list = models.CharField('附件的id列表，字段的值为: 1,2,3,4', max_length=20, null=True, blank=True)

    class Meta:
        db_table = 't_payment'
        verbose_name = '付款单表'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 付款单中 付款项目的模型类
class PaymentItemModel(BaseModel):
    # 冗余字段
    storage_code = models.CharField('采购入库单编号,不让用户填写', max_length=28)
    purchase_storage = models.ForeignKey('warehouse_info.PurchaseStorageModel', null=True, blank=True,
                                         on_delete=models.SET_NULL, verbose_name='采购入库单',related_name='payment_item')

    payment = models.ForeignKey('PaymentModel', null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name='付款单，不能改',related_name='item_list')
    should_money = models.DecimalField('应该 付款金额，最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0)
    this_money = models.DecimalField('本次 付款金额，最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0)

    remark = models.CharField('备注', max_length=512, blank=True, null=True)

    class Meta:
        db_table = 't_payment_item'
        verbose_name = '付款单中的 付款项目表'
        verbose_name_plural = verbose_name
        ordering = ['id']
