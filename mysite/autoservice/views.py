from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service, Car, Order
from .decorators import login_required_message
from .forms import ProfileForm

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request):
    return render(request, "profile.html", {"profile": request.user.profile})

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})

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


@login_required_message
def automobiliai(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "automobiliai.html", {"cars": page_obj})


@login_required_message
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


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "uzsakymai.html"
    context_object_name = "orders"
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Informacija bus pasiekiama po prisijungimo.")
        return super().dispatch(request, *args, **kwargs)


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = "uzsakymas.html"
    context_object_name = "order"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Informacija bus pasiekiama po prisijungimo.")
        return super().dispatch(request, *args, **kwargs)
