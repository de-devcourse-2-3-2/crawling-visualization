from django.db import models

class Style(models.Model):
    subject = models.CharField(max_length=64)
    date = models.DateField(null=False)
    category = models.CharField(max_length=16)
    views = models.IntegerField(default=0)
    URL = models.TextField(null=True)
    tag = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tb_style'

class Goods(models.Model):
    name = models.CharField(max_length=64, null=False)
    brand = models.CharField(max_length=64, null=False)
    origin_price = models.IntegerField(null=False)
    discounted_price = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=False)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tb_goods'

class StyleGoods(models.Model):
    id = models.AutoField(primary_key=True)  
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  
    style = models.ForeignKey(Style, on_delete=models.CASCADE)  

    class Meta:
        db_table = 'tb_style_goods'