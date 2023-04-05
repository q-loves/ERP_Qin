from django.db import models

# Create your models here.
# 采购单入库 模型类
from epr.utils.base_model import BaseModel


class PurchaseStorageModel(BaseModel):
    invoices_date = models.DateTimeField('单据日期',blank=True,null=True)
    number_code = models.CharField('单据编号,不让用户填写', max_length=28)
    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    discount = models.DecimalField('优惠率,最多精确到小数点后两位', max_digits=5, default=0, decimal_places=2, blank=True, null=True)
    discount_money = models.DecimalField('优惠金额(付款优惠),最多精确到小数点后两位', max_digits=10, default=0, decimal_places=2,
                                         blank=True,
                                         null=True)
    last_amount = models.DecimalField('优惠后总金额,最多精确到小数点后两位', max_digits=13, decimal_places=2, default=0, blank=True,
                                      null=True)
    other_money = models.DecimalField('其他费用,最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0, blank=True,
                                      null=True)
    this_payment = models.DecimalField('本次付款,最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0, blank=True,
                                       null=True)
    this_debt = models.DecimalField('本次欠款,最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0, blank=True,
                                    null=True)

    number_count = models.DecimalField('入库总数量,最多精确到小数点后两位', max_digits=10, decimal_places=2, blank=True, default=0)
    status = models.CharField('状态,0:未审核,1:已审核,2:部分付款,3:付款完成(包括欠款)', max_length=1, default='0')

    operator_user = models.ForeignKey('erp_system.UserModel', related_name='operator_in_list', null=True,
                                      on_delete=models.SET_NULL,
                                      verbose_name='入库操作人员，不能修改')
    # 增加一个冗余字段
    operator_user_name = models.CharField('操作人员的真实姓名', max_length=20, null=True, blank=True)
    check_user = models.ForeignKey('erp_system.UserModel', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='审核人员，不能修改')
    # 增加一个冗余字段
    check_user_name = models.CharField('操作人员的真实姓名', max_length=20, null=True, blank=True)

    account = models.ForeignKey('basic_info.SettlementAccountModel', null=True, on_delete=models.SET_NULL,
                                verbose_name='结算账户，审核之后不能改')

    supplier = models.ForeignKey('basic_info.SupplierModel', null=True, on_delete=models.SET_NULL,
                                 verbose_name='供应商，审核之后不能改')
    # 增加一个冗余字段
    supplier_name = models.CharField('供应商名称', max_length=30, null=True, blank=True)

    purchase = models.ForeignKey('purchase_info.PurchaseModel', null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='采购订单，审核之后不能改')

    attachment_list = models.CharField('附件的id列表，字段的值为: 1,2,3,4', max_length=20, null=True, blank=True)

    class Meta:
        db_table = 't_purchase_storage'
        verbose_name = '入库单表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 入库单中的货品（货品项目） 模型类
class PurchaseStorageItemModel(BaseModel):
    # 这些个也都是冗余字段, 减少查询的时候，表连接查询的次数
    name = models.CharField(max_length=20, verbose_name='货品名称')
    number_code = models.CharField('货品的编号或者批号', max_length=28, null=True, blank=True)
    specification = models.CharField('货品规格', max_length=50, null=True, blank=True)
    model_number = models.CharField('型号', max_length=50, null=True, blank=True)
    color = models.CharField('颜色', max_length=50, null=True, blank=True)
    units_name = models.CharField('单位名字', max_length=50, null=True, blank=True)
    units = models.ForeignKey('good_info.UnitsModel', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('good_info.GoodsCategoryModel', on_delete=models.SET_NULL, null=True, blank=True)
    category_name = models.CharField('货品类别名称', max_length=50, null=True, blank=True)

    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    purchase_count = models.DecimalField('入库数量,最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0)
    purchase_price = models.DecimalField('采购单价,最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0)
    purchase_money = models.DecimalField('采购金额,最多精确到小数点后两位', max_digits=10, decimal_places=2, default=0)

    purchase_storage = models.ForeignKey('PurchaseStorageModel', related_name='item_list', null=True, blank=True,
                                         on_delete=models.CASCADE,
                                         verbose_name='采购入库单')
    goods = models.ForeignKey('good_info.GoodsModel', null=True, on_delete=models.SET_NULL,
                              verbose_name='货品')

    warehouse = models.ForeignKey('basic_info.WarehouseModel', null=True, on_delete=models.SET_NULL,
                                  verbose_name='入库的仓库')
    warehouse_name = models.CharField('仓库名字', max_length=50, null=True)

    class Meta:
        db_table = 't_purchase_storage_items'
        verbose_name = '入库单的项目表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name + ' ' + self.specification
