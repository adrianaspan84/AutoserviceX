from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Service, Car, Order

def index(request):
    context = {
        "service_count": Service.objects.count(),
        "car_count": Car.objects.count(),
        "order_count": Order.objects.count(),
    }
    return render(request, "index.html", context)


def automobiliai(request):
    cars = Car.objects.all()
    return render(request, "automobiliai.html", {"cars": cars})


def automobilis(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "automobilis.html", {"car": car})


class OrderListView(generic.ListView):
    model = Order
    template_name = "uzsakymai.html"
    context_object_name = "orders"


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "uzsakymas.html"
    context_object_name = "order"
