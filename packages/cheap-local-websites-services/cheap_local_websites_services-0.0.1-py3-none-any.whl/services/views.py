from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Service

def services(request):
    services_list = Service.objects.order_by('id')
    context = {'services_list': services_list}
    return render(request, 'services/services.html', context)

def detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'services/services_detail.html', {'service': service})