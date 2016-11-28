from django.http import HttpResponse
from django.shortcuts import render
import json
from tasks import get_current_data

# Create your views here.
def data_view(request):
    return render(request, 'data.html')

def graphic_view(request):

    return render(request, 'template.html')

def data_api_view(request):
    data = get_current_data()
    speed = data[0]
    direction = data[1]
    peakGust = data[2]
    crossWindFlag = data[3]

    jsonResponse = {'windSpeed': speed, 'windDir': direction, 'peakGust': peakGust, 'crossWindFlag': crossWindFlag}

    data = json.dumps(jsonResponse)

    return HttpResponse(data, content_type='application/json')
    
