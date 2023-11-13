from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from plot.plot import Plot
from plot.utils import Utils

# Create your views here.

# style_brand_count():
#     return Json

# season_style_trend(season):
#     return Json


@api_view(['GET'])
def index(request) :
    return render(request,'index.html')

@api_view(['GET'])
def chart(request,chart_type):
    filename_img = ''
    if chart_type == 0 : # 스타일 동향 line chart
        # data = some_function()
        # Plot.line(data)
        filename_img = Plot.FILE_NAME_LINE
    elif chart_type == 1 : # 스타일 카테고리 별 브랜드 점유
        raw_data = category_brand_count()
        data = Utils.get_data_for_pie(raw_data)
        Plot.pie(data)
        filename_img = Plot.FILE_NAME_PIE
    elif chart_type == 2 : # 시즌 별 스타일 stacked bar chart
        raw_data = season_style_trend()
        data = Utils.get_data_for_stacked_bar(raw_data)
        Plot.stacked_bar(data)
        filename_img = Plot.FILE_NAME_STACKED_BAR
    return Response({'filename_img' : filename_img})

@api_view(['GET'])
def stylecat(request):
    data = popular_styles_by_category(request)
    return render(request, 'style_list.html', data)

@api_view(['GET'])
def stylesea(request) :
    data = top_styles_by_season(request)
    return render(request, 'style_list.html', data)