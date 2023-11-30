from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Style, StyleGoods, Goods
import logging
from logger import setLogOptions
from django.db.models import Sum
from django.db.models.functions import Coalesce
from plot.visualize import *
from plot.utils import *


setLogOptions()
logger = logging.getLogger(__name__)


@api_view(['GET'])
def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def chart(request):
    chart_type = request.GET.get('chart_type', 1)
    category = request.GET.get('category', '스포티')
    return Response({'filename_img': visualize(chart_type, category)})


def top_styles(request):
    """
    시즌 조회하는 기본 페이지 로직 구현
    """
    return render(request, 'top_styles.html')


def top_styles_by_season(request, season):
    """
    특정 시즌에서 조회수가 높은 순으로 Style을 조회
    """
    styles = (
        Style.objects.filter(season=season)
        .annotate(num_views=Count('views'))
        .order_by('-num_views')[:5]
    )

    context = {
        'styles_info': []
    }

    # 각 Style에 연관된 Goods 정보 조회
    for style in styles:
        goods_list = (
            StyleGoods.objects.filter(style=style)
            .select_related('goods')
            .annotate(
                price=Coalesce('goods__del_price', 'goods__price')  # del_price가 없으면 price를 사용
            )
        )

        goods_data = [{
            'name': sg.goods.name,
            'brand': sg.goods.brand,
            'price': sg.price
        } for sg in goods_list]

        # 컨텍스트에 스타일과 해당 상품 데이터 추가
        context['styles_info'].append({
            'subject': style.subject,
            'url': style.url,
            'goods': goods_data
        })

    # 템플릿에 컨텍스트 전달
    return render(request, 'top_styles_by_season.html', context)


def top_styles_c(request):
    """
    category 조회하는 기본 페이지 로직 구현
    """
    return render(request, 'top_styles_c.html')


def top_styles_by_category(request, category):
    """
    특정 카테고리에서 조회수가 높은 순으로 Style을 조회
    """
    styles = (
        Style.objects.filter(category=category)
        .annotate(num_views=Count('views'))
        .order_by('-num_views')[:5]
    )

    context = {
        'styles_info': []
    }

    # 각 Style에 연관된 Goods 정보 조회
    for style in styles:
        goods_list = (
            StyleGoods.objects.filter(style=style)
            .select_related('goods')
            .annotate(
                price=Coalesce('goods__del_price', 'goods__price')  # del_price가 없으면 price를 사용
            )
        )

        goods_data = [{
            'name': sg.goods.name,
            'brand': sg.goods.brand,
            'price': sg.price
        } for sg in goods_list]

        # 컨텍스트에 스타일과 해당 상품 데이터 추가
        context['styles_info'].append({
            'subject': style.subject,
            'url': style.url,
            'goods': goods_data
        })
    print('**** 전달될 값은', context)

    return render(request, 'top_styles_by_category.html', context)


@api_view(['GET'])
def stylecat(request):  # 뭘 하는지 함수명만 보고 알 수 없음. 바꿔야 함
    return render(request, 'style_list.html', popular_styles_by_category(request))

# 위 함수랑 아래 함수랑 3번째 인자 하나 차이 뿐이니 request 인자에 따라 다르게 하던지..
@api_view(['GET'])
def stylesea(request):  # 마찬가지임
    return render(request, 'style_list.html', top_styles_by_season(request))


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



# 이하는 render 또는 JSONResponse 반환 중 어느 것도 하지 않는 로직들
def visualize(chart_type, category):
    img_file_path, plot, utils = "", Plot(), Utils()
    if chart_type == '1':
        date_list, category_views_dict = get_data_for_page_1()
        img_file_path = plot.line(date_list, category_views_dict)

    # TODO: 와 오브젝트에서 봤을 때랑 똑같은 상황... 시각화 파트 리팩토링 하면서 같이 고칠 것
    elif chart_type == '2':  # 스타일 카테고리 별 브랜드 점유 Pie chart
        img_file_path = plot.pie(utils.get_data_for_pie(category, category_brand_count()))

    elif chart_type == '3':  # 시즌 별 스타일 stacked bar chart
        img_file_path = plot.stacked_bar(utils.get_data_for_stacked_bar(season_style_trend()))

    return img_file_path


def get_data_for_page_1():
    # 2022-01, 2022-02, .. , 2022-12
    date_list = []
    for month in range(1, 13):
        date_list.append(f"2022-{month:02}")

    category_list = ["걸리시", "고프코어", "골프", "댄디", "레트로", "로맨틱", "비즈니스캐주얼", "스트릿", "스포티", "시크", "아동복", "아메카지", "캐주얼",
                     "홈웨어"]
    category_views_dict = {category: [0]*12 for category in category_list}
    # category_이름: [월별 조회수]

    for i in range(12):  # 2022년 것만 하는 이유가 있다면 주석에 적는게 옳다
        query_result = Style.objects.filter(date__year=2022, date__month=i + 1) \
            .values('category') \
            .annotate(total_views=Sum('views')) \
            .order_by('-total_views')
        # query_result = {"category1이름" : 조회수1, "category2이름" : 조회수2, ...}

        for j in range(len(query_result)):
            category_name = query_result[j]['category']
            total_views = query_result[j]['total_views']
            category_views_dict[category_name][i] = total_views

    return date_list, category_views_dict


def category_brand_count():
    """
    스타일 선택 (ex . 아메카지)
    모든 브랜드 개수 확인
    """
    category_count_data = []
    for category in Style.objects.values('category').distinct():  # 이걸 저 위에 카테고리 하드 코딩된 곳에도 적용하는 게 맞지 않?
        category_name = category['category']
        goods_ids = StyleGoods.objects.filter(style__category=category_name).values_list('goods_id', flat=True)
        brand_count = Goods.objects.filter(id__in=goods_ids).values('brand').annotate(total=Count('brand'))
        category_count_data.append({
            'category': category_name,
            'brand_counts': list(brand_count)
        })

    return {
        'category_brand_counts': category_count_data
    }


def season_style_trend():
    """
    계절 별 조회수 10,000개 이상인 스타일에 대해서 카테고리별 개수 확인
    나타나는 값: 상위 5개 카테고리
    나머지에 대해서는 합해서 반환
    """
    # request 없이 계절 모두 구현 되도록 변경
    seasons = ['spring', 'summer', 'fall', 'winter']
    response_data = {'spring': {}, 'summer': {}, 'fall': {}, 'winter': {}}

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

        response_data[season] = {
            'top_categories': top_categories,
            'other_count': other_count
        }

    logger.info(
        f'********season_style_trend의 검색결과는 아래와 같습니다.\n'
        f'season : {season}\n'
        f'styles : {top_categories}\n'
        f'other_count : {other_count}\n'
    )
    return response_data
