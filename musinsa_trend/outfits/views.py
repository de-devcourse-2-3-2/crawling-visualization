from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from plot import plot

# Create your views here.

@api_view(['GET'])
def index(request) :
    context = {'img_url' : 'imgage03.png'}
    return render(request,'chart_with_js.html', context)

@api_view(['GET'])
def chart(request,chart_type):
    # plot.get_img()
    context = {'img_url' : 'image03.png'}
    return Response(context)

@api_view(['GET'])
def style(request, by):
    data = get_styles_by(by)
    return render(request, 'style.html', data)