from django.db import models

# Create your models here.

from erp.utils.base_model import BaseModel

# 货品(商品)类别模型类
class GoodsCategoryModel(BaseModel):
    name = models.CharField(max_length=100, verbose_name='类别名称')
    number_code = models.CharField('编号', max_length=28, unique=True)
    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    order_number = models.IntegerField('排序号码', default=100)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)

    class Meta:
        db_table = 't_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name
        ordering = ['order_number', 'id']

    def __str__(self):
        return self.name

# 计量单位模型类
class UnitsModel(BaseModel):
    basic_name = models.CharField(max_length=20, verbose_name='基本单位', unique=True)
    backup_name = models.CharField('副单位', max_length=20)
    remark = models.CharField('备注', max_length=512, blank=True, null=True)

    class Meta:
        db_table = 't_units'
        verbose_name = '计量单位'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return f'{self.basic_name}({self.backup_name})'

# 图片或者附件的模型类
class AttachmentModel(BaseModel):
    #choices
    # type_choices=(
    #     ('image','图片'),
    #     ('doc','word文档'),
    #     ('excel','excel文档'),
    #     ('zip','压缩文件'),
    #     ('other','其他文件')
    # )

    a_file=models.FileField(verbose_name='文件')
    # a_type=models.CharField(verbose_name='文件类型',choices=type_choices,blank=True,null=True,max_length=20)
    a_type=models.CharField(verbose_name='文件类型',blank=True,null=True,max_length=20)


    class Meta:
        db_table='t_attachment'
        verbose_name='附加文件'
        verbose_name_plural=verbose_name

# 货品库存 模型类
class GoodsInventoryModel(models.Model):
    init_inventory = models.DecimalField('期初库存数量', max_digits=10, decimal_places=2, default=0)
    cur_inventory = models.DecimalField('现在库存数量', max_digits=10, decimal_places=2, default=0)
    lowest_inventory = models.DecimalField('最低安全库存, 0表示不设置', max_digits=10, decimal_places=2, default=0)
    highest_inventory = models.DecimalField('最高安全库存,0表示不设置', max_digits=10, decimal_places=2, default=0)

    goods = models.ForeignKey('GoodsModel', related_name='inventory_list', on_delete=models.CASCADE, blank=True, null=True)
    warehouse = models.ForeignKey('basic_info.WarehouseModel', on_delete=models.CASCADE)
    # 冗余字段，主要目的：减少联表查询的次数
    warehouse_name = models.CharField('仓库的名称', max_length=50)

    class Meta:
        db_table = 't_goods_inventory'
        verbose_name = '货品库存表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.warehouse_name + str(self.id)


# 货品(商品)模型类
class GoodsModel(BaseModel):
    name = models.CharField(max_length=20, verbose_name='货品名称', unique=True)
    specification = models.CharField('规格', max_length=50, null=True, blank=True)
    model_number = models.CharField('型号', max_length=50, null=True, blank=True)
    color = models.CharField('颜色', max_length=50, null=True, blank=True)
    basic_weight = models.CharField('基础重量', max_length=50, null=True, blank=True)
    expiration_day = models.IntegerField('保质期', null=True, blank=True)
    remark = models.CharField('备注', max_length=512, blank=True, null=True)
    number_code = models.CharField('编号或者批号', max_length=28, unique=True)
    purchase_price = models.DecimalField('采购价', max_digits=10, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    retail_price = models.DecimalField('零售价', max_digits=10, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    sales_price = models.DecimalField('销售价', max_digits=10, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    lowest_price = models.DecimalField('最低售价', max_digits=10, decimal_places=2, blank=True, null=True)  # 精确到小数点后两位
    order_number = models.IntegerField('排序号码', default=100)

    units = models.ForeignKey('UnitsModel', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('GoodsCategoryModel', on_delete=models.SET_NULL, null=True, blank=True)
    images_list = models.CharField('商品图片所对应的id列表', max_length=20, null=True, blank=True)  # 字段的值为: 1,2,3,4

    class Meta:
        db_table = 't_goods'
        verbose_name = '货品表'
        verbose_name_plural = verbose_name
        ordering = ['order_number', 'id']

    def __str__(self):
        return self.name
