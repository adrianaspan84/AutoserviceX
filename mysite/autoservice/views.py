from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Service, Car
from .decorators import login_required_message
from .forms import ProfileForm
from django.contrib.auth import login
from .forms import SignupForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib import messages


from .models import Order
from .forms import OrderCommentForm



def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatinis prisijungimas po registracijos
            messages.success(request, "Registracija sėkminga!")
            return redirect("index")
    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})



@login_required
def add_comment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = OrderCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.order = order
            comment.user = request.user
            comment.save()
            messages.success(request, "Komentaras pridėtas!")
            return redirect("uzsakymas", pk=order_id)
        else:
            # forma neteisinga → parodyti klaidas tame pačiame puslapyje
            return render(request, "uzsakymas.html", {
                "order": order,
                "form": form,
            })

    return redirect("uzsakymas", pk=order_id)

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "user_orders.html", {"orders": orders})

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


class OrderDetailView(DetailView):
    model = Order
    template_name = "uzsakymas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = OrderCommentForm()  # ← ŠITA EILUTĖ YRA PRIVALOMA
        return context

