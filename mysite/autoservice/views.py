from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Service, Car, Order

def logout_view(request):
    logout(request)
    return redirect('/')

def services(request):
    services = Service.objects.all()
    return render(request, "services.html", {"services": services})


def index(request):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "service_count": Service.objects.count(),
        "car_count": Car.objects.count(),
        "order_count": Order.objects.count(),
        "num_visits": num_visits,
    }
    return render(request, "index.html", context)



def automobiliai(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "automobiliai.html", {"cars": page_obj})



def automobilis(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, "automobilis.html", {"car": car})


def car_search(request):
    query = request.GET.get("q", "")
    results = Car.objects.filter(
        Q(make__icontains=query) |
        Q(model__icontains=query) |
        Q(client_name__icontains=query) |
        Q(license_plate__icontains=query) |
        Q(vin_code__icontains=query)
    )
    return render(request, "car_search.html", {"query": query, "cars": results})


class OrderListView(generic.ListView):
    model = Order
    template_name = "uzsakymai.html"
    context_object_name = "orders"
    paginate_by = 5

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "uzsakymas.html"
    context_object_name = "order"
