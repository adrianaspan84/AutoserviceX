from django.contrib import admin
from .models import Service, Car, Order, OrderLine


# --- Paslaugos ---
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    search_fields = ["name"]  # reikalinga autocomplete


# --- Automobiliai ---
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["make", "model", "client_name", "license_plate", "vin_code"]
    list_filter = ["make", "model", "client_name"]
    search_fields = ["license_plate", "vin_code", "client_name"]


# --- Užsakymo eilutės (inline) ---
class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ("service", "quantity", "status")
    can_delete = True


# --- Užsakymai ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "car", "status", "total")
    list_editable = ("status",)
    list_filter = ("status", "date")
    search_fields = ("car__make", "car__model", "car__license_plate")
    inlines = [OrderLineInline]


# --- Užsakymo eilutės (atskiras meniu punktas) ---
@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ("order", "service", "quantity", "status")
    list_filter = ("status", "service")
    search_fields = ("order__id", "service__name")
    autocomplete_fields = ("order", "service")
