from django.shortcuts import render

# Create your views here.
def data_view(request):
    return render(request, 'data.html')
