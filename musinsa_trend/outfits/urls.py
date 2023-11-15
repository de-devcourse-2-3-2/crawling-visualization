import os
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from . import views

# static file url example :
# www.example.com:8000/static/media/image01.png

urlpatterns = [
    path('index/', views.index, name='index'),
    path('chart', views.chart, name='chart'),
    path('styles_by_category', views.stylecat, name='styles_by_season'),
    path('styles_by_season', views.stylesea, name='styles_by_season'),
    
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
]

# urlpatterns = [
    # path('category_brand_count/', views.category_brand_count, name='category_brand_count'),
    # path('season-style-trend/', views.season_style_trend, name='season_style_trend'),
    # path('popular-styles/', views.popular_styles_by_category, name='popular_styles_by_category'),
    # path('top-styles/', views.top_styles_by_season, name='top_styles_by_season'),
# ]