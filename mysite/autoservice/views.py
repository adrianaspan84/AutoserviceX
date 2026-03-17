from django.shortcuts import render
from .models import Service, Car, Order

def index(request):
    context = {
        "service_count": Service.objects.count(),
        "car_count": Car.objects.count(),
        "order_count": Order.objects.count(),
    }
    return render(request, "index.html", context)
