from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from plot import plot

# Create your views here.

@api_view(['GET'])
def index(request) :
    return render(request,'index.html')

@api_view(['GET'])
def chart(request,chart_type):
    # plot.get_img()
    context = {'img_url' : 'image03.png'}
    return Response(context)

@api_view(['GET'])
def style(request, by):
    get_styles_by(by)
    return render(request, 'style_list.html', data)