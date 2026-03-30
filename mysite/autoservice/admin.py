from django.contrib import admin
from .models import Profile, Service, Car, Order, OrderLine


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar", "bio")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("make", "model", "license_plate", "client_name")
    search_fields = ("make", "model", "license_plate", "client_name")


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "car", "date", "return_date", "status", "total", "is_overdue_display")
    list_filter = ("status", "date", "return_date", "user")
    search_fields = ("id", "car__license_plate", "car__make", "car__model", "user__username")
    inlines = [OrderLineInline]

    def is_overdue_display(self, obj):
        return "TAIP" if obj.is_overdue else "NE"
    is_overdue_display.short_description = "Vėluoja?"
