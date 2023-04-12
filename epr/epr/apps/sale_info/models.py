from django.db import models

# Create your models here.
# 销售订单 模型类
from epr.utils.base_model import BaseModel


class SaleModel(BaseModel):
    invoices_date = models.DateTimeField('单据日期',blank=True,null=True)
    number_code = models.CharField('单据编号,不让用户填写', max_length=28)
    discount = models.DecimalField('优惠率,最多精确到小数点后两位', max_digits=5, decimal_places=2, blank=True, default=0)
    discount_money = models.DecimalField('优惠金额(付款优惠),最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True,
                                         default=0)
    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    last_amount = models.DecimalField('优惠后总金额,最多精确到小数点后两位', max_digits=13, decimal_places=2, blank=True, default=0)
    deposit = models.DecimalField('收取定金,最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True, default=0)

    number_count = models.DecimalField('销售数量,最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True, default=0)
    status = models.CharField('状态,0:未审核,1:已审核,2:部分发货,3:全部发货,4:完成销售,5:已收定金', max_length=1, default='0')

    operator_user = models.ForeignKey('erp_system.UserModel', related_name='operator_sale_list', null=True,
                                      blank=True, on_delete=models.SET_NULL,
                                      verbose_name='销售操作人员，不能修改')
    # 增加一个冗余字段
    operator_user_name = models.CharField('销售人员的真实姓名', max_length=20, null=True, blank=True)
    check_user = models.ForeignKey('erp_system.UserModel', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='审核人员，不能修改')
    # 增加一个冗余字段
    check_user_name = models.CharField('审核人员的真实姓名', max_length=20, null=True, blank=True)

    account = models.ForeignKey('basic_info.SettlementAccountModel', null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name='结算账户，审核之后不能改')

    customer = models.ForeignKey('basic_info.CustomerModel', null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='客户，审核之后不能改')
    # 增加一个冗余字段
    customer_name = models.CharField('客户名称', max_length=30, null=True, blank=True)

    attachment_list = models.CharField('附件的id列表，字段的值为: 1,2,3,4', max_length=20, null=True, blank=True)

    class Meta:
        db_table = 't_sales'
        verbose_name = '销售表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 销售订单（货品项目） 模型类
class SaleItemModel(BaseModel):
    # 这些个也都是冗余字段, 减少查询的时候，表连接查询的次数
    name = models.CharField(max_length=20, verbose_name='货品名称')
    number_code = models.CharField('货品的编号或者批号', max_length=28, null=True, blank=True)
    specification = models.CharField('货品规格', max_length=50, null=True, blank=True)
    model_number = models.CharField('型号', max_length=50, null=True, blank=True)
    color = models.CharField('颜色', max_length=50, null=True, blank=True)
    units_name = models.CharField('单位名字', max_length=50, null=True, blank=True)
    units = models.ForeignKey('good_info.UnitsModel', on_delete=models.SET_NULL, null=True, blank=True)
    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    sales_count = models.DecimalField('销售数量,最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0)
    sales_price = models.DecimalField('销售单价,最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0)
    sales_money = models.DecimalField('销售金额,最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0)

    sale = models.ForeignKey('SaleModel', related_name='item_list', null=True, blank=True,
                             on_delete=models.CASCADE,
                             verbose_name='销售单')
    goods = models.ForeignKey('good_info.GoodsModel', null=True, on_delete=models.SET_NULL,
                              verbose_name='货品')

    class Meta:
        db_table = 't_sales_items'
        verbose_name = '销售订单的项目表'
        verbose_name_plural = verbose_name
        ordering = ['id']
