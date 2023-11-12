from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from plot import plot

# Create your views here.
# def style_brand_count(style_id):
#     return Json

# def season_style_trend(season):
#     return Json


@api_view(['GET'])
def index(request) :
    return render(request,'index.html')

@api_view(['GET'])
def chart(request,chart_type):
    iilename_img = ''
    if chart_type == 1 : # 스타일 동향 line chart
        # data = some_function()
        # Plot.stacked_bar(data)
        filename_img = Plot.FILE_NAME_LINE
    elif chart_type == 2 : # 시즌 별 스타일 stacked bar chart
        data = season_style_trend()
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