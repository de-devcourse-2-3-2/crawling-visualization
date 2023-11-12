from django.shortcuts import render
from django.db.models import Count
from .models import Style, StyleGoods, Goods
from django.http import JsonResponse

import logging
from logger import setLogOptions

setLogOptions()
logger = logging.getLogger(__name__)

def style_brand_count(request):
    """
    스타일 선택 (ex . 아메카지)
    모든 브랜드 개수 확인
    """
    styles = list(Style.objects.all().values('id', 'subject'))
    brand_count_data = None

    if 'style' in request.GET:
        style_id = request.GET['style']
        selected_style = Style.objects.get(pk=style_id)
        goods_ids = StyleGoods.objects.filter(style=selected_style).values_list('goods_id', flat=True)
        brand_count = Goods.objects.filter(id__in=goods_ids).values('brand').annotate(total=Count('brand'))
        brand_count_data = list(brand_count) 

    logger.info(f'********style_brand_count의 검색결과는 아래와 같습니다.\n'f'styles : {styles} -> brand_count : {brand_count_data}')


    return JsonResponse({
        'styles': styles,
        'brand_count': brand_count_data
    })

def season_style_trend():
    """
    계절 별 조회수 10,000개 이상인 스타일에 대해서 카테고리별 개수 확인
    나타나는 값: 상위 5개 카테고리
    나머지에 대해서는 합해서 반환
    """
    # request 없이 계절 모두 구현 되도록 변경 
    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    response_data = {}

    for season in seasons:
        top_categories = list(Style.objects.filter(
            season=season,
            views__gte=10000
        ).values('category').annotate(count=Count('category')).order_by('-count')[:5])

        other_count = Style.objects.filter(
            season=season,
            views__gte=10000
        ).exclude(
            category__in=[category['category'] for category in top_categories]
        ).count()

    logger.info(
        f'********season_style_trend의 검색결과는 아래와 같습니다.\n'
        f'styles : {top_categories}\n'
        f'other_count : {other_count}\n'
        f'season : {season}'
    )

    response_data = {
        'top_categories': top_categories,
        'other_count': other_count,
    }
    # Json 형태로 return 변경
    return response_data

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