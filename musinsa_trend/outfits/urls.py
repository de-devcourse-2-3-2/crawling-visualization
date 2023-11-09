from django.urls import path
from . import views

urlpatterns = [
    path('style-brand-count/', views.style_brand_count, name='style_brand_count'),
]
