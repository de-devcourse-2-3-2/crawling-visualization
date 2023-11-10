from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from plot import plot

# Create your views here.

@api_view(['GET'])
def index(request) :
    context = chart(request, 1)
    return render(request,'index.html', context)

@api_view(['GET'])
def chart(request, chart_type):
    data = {'img_url' : "chart/image01.png"}
    if chart_type == 1 :
        #data = plot.chart()
        pass
    return Response(data)

@api_view(['GET'])
def style(request, by):
    data = get_styles_by(by)
    return render(request, 'style.html', data)