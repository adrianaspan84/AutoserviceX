from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path("", views.index, name="index"),
    path("automobiliai/", views.automobiliai, name="automobiliai"),
    path("automobiliai/<int:car_id>/", views.automobilis, name="automobilis"),
    path("services/", views.services, name="services"),
    path("search/", views.car_search, name="car_search"),

    path("uzsakymai/", views.OrderListView.as_view(), name="uzsakymai"),
    path("uzsakymai/<int:pk>/", views.OrderDetailView.as_view(), name="uzsakymas"),

    path("logout/", logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]
