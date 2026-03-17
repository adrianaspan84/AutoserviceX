from django.contrib import admin
from .models import Service, Car, Order, OrderLine


# --- Užsakymo eilutės inline ---
class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0


# --- Paslaugos ---
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


# --- Automobiliai ---
class CarAdmin(admin.ModelAdmin):
    list_display = ["make", "model", "client_name", "license_plate", "vin_code"]
    list_filter = ["client_name", "make", "model"]
    search_fields = ["license_plate", "vin_code"]


# --- Užsakymo eilutės ---
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ["order", "service", "quantity", "line_sum"]


# --- Užsakymai ---
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "car", "date", "total"]
    inlines = [OrderLineInline]


# --- Registracija ---
admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
