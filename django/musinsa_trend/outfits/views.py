from django.shortcuts import render
from django.db.models import Count
from .models import Style, StyleGoods, Goods

def style_brand_count(request):
    styles = Style.objects.all()
    brand_count = None

    if 'style' in request.GET:
        style_id = request.GET['style']
        selected_style = styles.get(pk=style_id)
        goods_ids = StyleGoods.objects.filter(style=selected_style).values_list('goods_id', flat=True)
        brand_count = Goods.objects.filter(id__in=goods_ids).values('brand').annotate(total=Count('brand'))

    return render(request, 'test.html', {
        'styles': styles,
        'brand_count': brand_count
    })
