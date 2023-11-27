import os
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chart', views.chart, name='chart'),
    
    # Generic schema view of app
    path('schema_view/', get_schema_view(
        title="Musinsa Trend Analyzer",
        description="All APIs",
        version="1.0.0"
    ), name='schema_view'),

    # Openapi schema view with UI
    path('openapi/', TemplateView.as_view(
        template_name='openapi_schema.html',
        extra_context={'schema_url':'schema_view'}
    ), name='openapi_schema_view'),
    # 기본 페이지 경로: 계절이 선택되지 않았을 때
    path('top-styles/', views.top_styles, name='top_styles'),
    # 계절이 선택되었을 때의 경로
    path('top-styles/<str:season>/', views.top_styles_by_season, name='top_styles_by_season'),
    # 기본 페이지 경로: 카테고리가 선택되지 않았을 때
    path('top-styles-c/', views.top_styles_c, name='top_styles_c'),
    # 카테고리가 선택되었을 때의 경로
    path('top-styles-c/<str:category>/', views.top_styles_by_category, name='top_styles_by_category'),
]
