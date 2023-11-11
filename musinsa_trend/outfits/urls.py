from django.urls import path
from . import views

urlpatterns = [
    path('style-brand-count/', views.style_brand_count, name='style_brand_count'),
    path('season-style-trend/', views.season_style_trend, name='season_style_trend'),
    path('popular-styles/', views.popular_styles_by_category, name='popular_styles_by_category'),
    path('top-styles/', views.top_styles_by_season, name='top_styles_by_season'),
]
