from django.contrib import admin
from django.utils.html import format_html
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
    readonly_fields = ("line_sum",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # Ką rodome sąraše
    list_display = (
        "colored_id",
        "user",
        "client_name",
        "car",
        "date",
        "return_date",
        "status",
        "total",
        "is_overdue_display",
    )

    # Leidžiame redaguoti USER ir STATUS tiesiog sąraše
    list_editable = (
        "user",
        "status",
    )

    # Nuoroda tik ant ID
    list_display_links = ("colored_id",)

    # Filtrai
    list_filter = ("status", "date", "return_date", "user")

    # Paieška
    search_fields = (
        "id",
        "car__license_plate",
        "car__make",
        "car__model",
        "car__client_name",
        "user__username",
    )

    inlines = [OrderLineInline]

    # Laukai redagavimo formoje
    fields = (
        "user",
        "car",
        "date",
        "return_date",
        "status",
        "total",
    )

    readonly_fields = ("total",)

    # Kliento vardas
    def client_name(self, obj):
        return obj.car.client_name
    client_name.short_description = "Klientas"

    # Vėlavimo rodymas
    def is_overdue_display(self, obj):
        return "TAIP" if obj.is_overdue else "NE"
    is_overdue_display.short_description = "Vėluoja?"

    # Raudona eilutė, jei vėluoja
    def colored_id(self, obj):
        if obj.is_overdue:
            return format_html(
                '<span style="color: red; font-weight: bold;">#{}</span>',
                obj.id
            )
        return f"#{obj.id}"

    colored_id.short_description = "ID"
