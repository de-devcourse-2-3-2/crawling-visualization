from django.urls import path
from .views import get_brand_count_by_style

urlpatterns = [
    path('styles/<str:style_subject>/brands/count/', get_brand_count_by_style, name='brand-count-by-style'),
]
