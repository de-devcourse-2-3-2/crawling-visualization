from django.db import models
from django.utils import timezone

# id 필드를 한 군데도 코딩을 안했다. 스키마에 아이디가 있는데도 코딩 안해도 문제는 안생기는..?
class Style(models.Model):
    subject = models.CharField(max_length=64)
    date = models.DateField(null=False)
    category = models.CharField(max_length=64)
    views = models.IntegerField(default=0)
    season = models.CharField(max_length=16)
    url = models.TextField(null=True)
    tag = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'style'

class Goods(models.Model):
    name = models.CharField(max_length=128, null=False)
    brand = models.CharField(max_length=128, null=False)
    price = models.IntegerField(null=False)
    del_price = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=False)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'goods'

class StyleGoods(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'style_goods'
        # unique_together = (('style_id', 'goods_id'),)