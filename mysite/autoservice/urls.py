from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("automobiliai/", views.automobiliai, name="automobiliai"),
    path("automobiliai/paieska/", views.car_search, name="car_search"),
    path("automobiliai/<int:car_id>/", views.automobilis, name="automobilis"),
    path("uzsakymai/", views.OrderListView.as_view(), name="uzsakymai"),
    path("uzsakymai/<int:pk>/", views.OrderDetailView.as_view(), name="uzsakymas"),
    path("paslaugos/", views.services, name="services"),

]
