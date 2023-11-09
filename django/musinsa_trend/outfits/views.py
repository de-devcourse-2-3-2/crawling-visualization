from django.http import JsonResponse
from .models import Style, Goods, StyleGoods
from django.db.models import Count

def get_brand_count_by_style(request, style_subject):
    """
    스타일별 브랜드 개수 조회 기능 
    """
    style = Style.objects.get(subject=style_subject)
    goods_ids = StyleGoods.objects.filter(style=style).values_list('goods', flat=True)
    brand_count = Goods.objects.filter(id__in=goods_ids).values('brand').annotate(total=Count('brand')).order_by('brand')

    return JsonResponse(list(brand_count), safe=False)
