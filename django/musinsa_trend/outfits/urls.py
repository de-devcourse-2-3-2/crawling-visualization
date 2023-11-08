from django.urls import path
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('openapi_schema/', get_schema_view(
        title="Musinsa Trend Analyzer",
        description="All APIs",
        version="1.0.0"
    ), name='openapi_schema'),
    path('openapi/', TemplateView.as_view(
        template_name='openapi_schema.html',
        extra_context={'schema_url':'openapi_schema'}
    ), name='openapi_schema_view'),
]