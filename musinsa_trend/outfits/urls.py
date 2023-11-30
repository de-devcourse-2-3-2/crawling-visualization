import os
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from .views import *

# static file url example :
# www.example.com:8000/static/media/image01.png

urlpatterns = [
    path('index/', index, name='index'),
    path('chart', chart, name='chart'),  # TODO: TDD 책에 나와 있던 대로 '/' 추가 여부 통일하기
    # TODO: 인자를 여기가 아닌 (스프링부트 기준) controller 단에서 처리하도록 만들 수 있는지 알아보기
    path('top-styles/', top_styles, name='top_styles'),  # 계절이 선택되지 않았을 때
    path('top-styles/<str:season>/', top_styles_by_season, name='top_styles_by_season'),  # 계절이 선택 됐을 때
    path('top-styles-c/', top_styles_c, name='top_styles_c'),  # 카테고리가 선택되지 않았을 때
    path('top-styles-c/<str:category>/', top_styles_by_category, name='top_styles_by_category'),  # 카테고리가 선택 됐을 때


    path('schema_view/', get_schema_view(
        title="Musinsa Trend Analyzer",
        description="All APIs",
        version="1.0.0"
    ), name='schema_view'),

    path('openapi/', TemplateView.as_view(
        template_name='openapi_schema.html',
        extra_context={'schema_url':'schema_view'}
    ), name='openapi_schema_view'),

    # path('styles_by_category', views.stylecat, name='styles_by_season'),
    # path('styles_by_season', views.stylesea, name='styles_by_season'),
]
