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

def season_style_trend(request):
    """
    계절 별 조회수 10,000개에 대해서 카테고리별 개수 확인
    나타나는 값 : 상위 5개
    나머지에 대해서는 합해서 return
    -> 총 6개 값 return 
    """
    season = request.GET.get('season', 'Spring')
    styles = Style.objects.filter(
        season=season,
        views__gte=10000
    ).values('category').annotate(count=Count('category')).order_by('-count')[:5]

    # 나머지 카테고리에 대한 개수
    other_count = Style.objects.filter(
        season=season,
        views__gte=10000
    ).exclude(
        category__in=[style['category'] for style in styles]
    ).count()

    return render(request, 'test2.html', {
        'styles': styles,
        'other_count': other_count,
        'season': season
    })