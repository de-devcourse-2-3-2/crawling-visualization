from django.urls import path
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('chart/', views.chart, {'chart_type': 0}, name='chart'),
    path('style/', views.style, {'by': 'season'}, name='style'),
    
    # Schema view of app
    path('schema_view/', get_schema_view(
        title="Musinsa Trend Analyzer",
        description="All APIs",
        version="1.0.0"
    ), name='schema_view'),

    # Openapi schema view UI
    path('openapi/', TemplateView.as_view(
        template_name='openapi_schema.html',
        extra_context={'schema_url':'schema_view'}
    ), name='openapi_schema_view'),
]