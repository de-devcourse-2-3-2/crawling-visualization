from django.shortcuts import render
from django.db.models import Count
from .models import Style, StyleGoods, Goods
from django.http import JsonResponse

import logging
from logger import setLogOptions

setLogOptions()
logger = logging.getLogger(__name__)

def style_brand_count(request):
    styles = Style.objects.all()
    brand_count = None

    if 'style' in request.GET:
        style_id = request.GET['style']
        selected_style = styles.get(pk=style_id)
        goods_ids = StyleGoods.objects.filter(style=selected_style).values_list('goods_id', flat=True)
        brand_count = Goods.objects.filter(id__in=goods_ids).values('brand').annotate(total=Count('brand'))

    logger.info(f'*******{request}, style : {styles}, brand_count : {brand_count}')
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

    logger.info(f'*******{request}, style : {styles}, brand_count : {other_count}')
    return render(request, 'test2.html', {
        'styles': styles,
        'other_count': other_count,
        'season': season
    })

def popular_styles_by_category(request):
    """
    카테고리에 대한 최상위 스타일 5개 조회
    해당 스타일에 있는 사진, 그 스타일에 있는 상품 list 조회
    """
    category_name = request.GET.get('category')
    if category_name:
        top_styles = Style.objects.filter(category=category_name).order_by('-views')[:5]

        results = [
            {
                'subject': style.subject,
                'views': style.views,
                'url': style.URL,
                'goods_list': list(StyleGoods.objects.filter(style=style).values('goods__name', 'goods__brand'))
            } for style in top_styles
        ]
        logger.info(f'*******popular_styles_by_category : {results} 이 검색되었습니다.')
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({'error': '카테고리가 지정되지 않았습니다.'}, status=400)

def top_styles_by_season(request):
    """
    시즌에 대한 최상위 스타일 5개 조회
    해당 스타일에 있는 사진, 그 스타일에 있는 상품 list 조회
    """
    season_name = request.GET.get('season')
    if season_name:
        top_styles = Style.objects.filter(season=season_name).order_by('-views')[:5]

        results = [
            {
                'subject': style.subject,
                'views': style.views,
                'url': style.URL,
                'style_goods': [
                    {'name': sg.goods.name, 'brand': sg.goods.brand}
                    for sg in StyleGoods.objects.filter(style=style)
                ]
            } for style in top_styles
        ]
        logger.info(f'*******top_styles_by_season : {results} 이 검색되었습니다.')
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({'error': 'need to choice season.'}, status=400)