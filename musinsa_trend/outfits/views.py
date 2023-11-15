from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Count
from .models import Style, StyleGoods, Goods
import logging
from logger import setLogOptions

setLogOptions()
logger = logging.getLogger(__name__)

# # Create your views here.

# # style_brand_count():
# #     return Json

# # season_style_trend(season):
# #     return Json


# @api_view(['GET'])
# def index(request) :
#     return render(request,'index.html')

# @api_view(['GET'])
# def chart(request):
#     filename_img = ''
#     msg = ''
#     plot = Plot()
#     utils = Utils()
#     chart_type = request.GET.get('chart_type', 1)
#     category = request.GET.get('category', '스포티')
#     if chart_type == '1' : # 스타일 동향 line chart
#         # 로직이 구현되지 않음
#         # data = some_function()
#         # Plot.line(data)
#         filename_img = Plot.FILE_NAME_LINE
#     elif chart_type == '2' : # 스타일 카테고리 별 브랜드 점유 Pie chart
#         raw_data = category_brand_count()
#         # Or you use sample data with alternative code below
#         # raw_data = Utils.SAMPLE_PIE
#         data = Utils.get_data_for_pie(category,raw_data)
#         if plot.pie(data) :
#             filename_img = Plot.FILE_NAME_PIE
#     elif chart_type == '3' : # 시즌 별 스타일 stacked bar chart
#         raw_data = season_style_trend()
#         # print('-'*50)
#         # print(raw_data)
#         # print('-'*50)
#         # Or you use sample data with alternative code below
#         # raw_data = Utils.SAMPLE_STACKED_BAR
#         data = utils.get_data_for_stacked_bar(raw_data)
#         if plot.stacked_bar(data) :
#             filename_img = plot.FILE_NAME_STACKED_BAR
#     return Response({'filename_img' : filename_img})

# @api_view(['GET'])
# def stylecat(request):
#     data = popular_styles_by_category(request)
#     return render(request, 'style_list.html', data)

# @api_view(['GET'])
# def stylesea(request) :
#     data = top_styles_by_season(request)
#     return render(request, 'style_list.html', data)

# def category_brand_count():
#     """
#     스타일 선택 (ex . 아메카지)
#     모든 브랜드 개수 확인
#     """
    
#     category_count_data = []
#     for category in Style.objects.values('category').distinct():
#         category_name = category['category']
#         goods_ids = StyleGoods.objects.filter(style__category=category_name).values_list('goods_id', flat=True)
#         brand_count = Goods.objects.filter(id__in=goods_ids).values('brand').annotate(total=Count('brand'))
#         category_count_data.append({
#             'category': category_name,
#             'brand_counts': list(brand_count)
#         })

#     return {
#         'category_brand_counts': category_count_data
#     }

# def season_style_trend():
#     """
#     계절 별 조회수 10,000개 이상인 스타일에 대해서 카테고리별 개수 확인
#     나타나는 값: 상위 5개 카테고리
#     나머지에 대해서는 합해서 반환
#     """
#     # request 없이 계절 모두 구현 되도록 변경 
#     seasons = ['spring', 'summer', 'fall', 'winter']
#     response_data = {'spring': {} , 'summer' : {}, 'fall' : {}, 'winter' : {}}

#     for season in seasons:
#         top_categories = list(Style.objects.filter(
#             season=season,
#             views__gte=10000
#         ).values('category').annotate(count=Count('category')).order_by('-count')[:5])

#         other_count = Style.objects.filter(
#             season=season,
#             views__gte=10000
#         ).exclude(
#             category__in=[category['category'] for category in top_categories]
#         ).count()

#         response_data[season] = {
#             'top_categories': top_categories,
#             'other_count': other_count
#             }

#     logger.info(
#         f'********season_style_trend의 검색결과는 아래와 같습니다.\n'
#         f'season : {season}\n'
#         f'styles : {top_categories}\n'
#         f'other_count : {other_count}\n'
#     )
#     return response_data

# def popular_styles_by_category(request):
#     """
#     카테고리에 대한 최상위 스타일 5개 조회
#     해당 스타일에 있는 사진, 그 스타일에 있는 상품 list 조회
#     """
#     category_name = request.GET.get('category')
#     if category_name:
#         top_styles = Style.objects.filter(category=category_name).order_by('-views')[:5]

#         results = [
#             {
#                 'subject': style.subject,
#                 'views': style.views,
#                 'url': style.URL,
#                 'goods_list': list(StyleGoods.objects.filter(style=style).values('goods__name', 'goods__brand'))
#             } for style in top_styles
#         ]
#         logger.info(f'*******popular_styles_by_category : {results} 이 검색되었습니다.')
#         return JsonResponse(results, safe=False)
#     else:
#         return JsonResponse({'error': '카테고리가 지정되지 않았습니다.'}, status=400)

# def top_styles_by_season(request):
#     """
#     시즌에 대한 최상위 스타일 5개 조회
#     해당 스타일에 있는 사진, 그 스타일에 있는 상품 list 조회
#     """
#     season_name = request.GET.get('season')
#     if season_name:
#         top_styles = Style.objects.filter(season=season_name).order_by('-views')[:5]

#         results = [
#             {
#                 'subject': style.subject,
#                 'views': style.views,
#                 'url': style.URL,
#                 'style_goods': [
#                     {'name': sg.goods.name, 'brand': sg.goods.brand}
#                     for sg in StyleGoods.objects.filter(style=style)
#                 ]
#             } for style in top_styles
#         ]
#         logger.info(f'*******top_styles_by_season : {results} 이 검색되었습니다.')
#         return JsonResponse(results, safe=False)
#     else:
#         return JsonResponse({'error': 'need to choice season.'}, status=400)

#########################################       NEW      #################################################
from django.shortcuts import render
from .models import Style, StyleGoods, Goods
from django.db.models import Count

def top_styles(request):
    # 여기에 기본 페이지 로직 구현
    return render(request, 'top_styles.html')

def top_styles_by_season(request, season):
    styles = Style.objects.filter(season=season).annotate(num_views=Count('views')).order_by('-num_views')[:5]
    context = {'styles': []}
    for style in styles:
        goods_list = StyleGoods.objects.filter(style=style).select_related('goods')[:3]
        goods_data = [{
            'name': sg.goods.name,
            'brand': sg.goods.brand,
            'price': sg.goods.discounted_price if sg.goods.discounted_price else sg.goods.origin_price
        } for sg in goods_list]
        context['styles'].append({'style': style, 'goods': goods_data})
    return render(request, 'top_styles_by_season.html', context)
