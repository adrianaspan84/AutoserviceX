from django.db import models
from django.db import models
from django.contrib.auth.models import User

def user_avatar_path(instance, filename):
    return f"avatars/user_{instance.user.id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_avatar_path, default="avatars/default.png", blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profilis: {self.user.username}"




# -------------------------
# PASLAUGA
# -------------------------
class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=200)
    price = models.FloatField(verbose_name="Kaina")

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

    def __str__(self):
        return f"{self.name} ({self.price} €)"


# -------------------------
# AUTOMOBILIS
# -------------------------
class Car(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=100)
    model = models.CharField(verbose_name="Modelis", max_length=100)
    license_plate = models.CharField(verbose_name="Valstybinis numeris", max_length=20)
    vin_code = models.CharField(verbose_name="VIN kodas", max_length=50)
    client_name = models.CharField(verbose_name="Klientas", max_length=200)
    photo = models.ImageField(upload_to="car_photos/", null=True, blank=True, verbose_name="Nuotrauka")

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


# -------------------------
# UŽSAKYMAS
# -------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ("naujas", "Naujas"),
        ("vykdomas", "Vykdomas"),
        ("baigtas", "Baigtas"),
        ("atsauktas", "Atšauktas"),
    ]

    date = models.DateField(verbose_name="Data")
    car = models.ForeignKey("Car", verbose_name="Automobilis", on_delete=models.CASCADE)
    status = models.CharField(
        verbose_name="Statusas",
        max_length=20,
        choices=STATUS_CHOICES,
        default="naujas"
    )

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"

    def total(self):
        return sum(line.line_sum() for line in self.lines.all())

    total.short_description = "Bendra suma"

    def __str__(self):
        return f"Užsakymas #{self.id} – {self.car}"


# -------------------------
# UŽSAKYMO EILUTĖ
# -------------------------
class OrderLine(models.Model):
    STATUS_CHOICES = [
        ("laukiama", "Laukiama"),
        ("vykdoma", "Vykdoma"),
        ("baigta", "Baigta"),
    ]

    order = models.ForeignKey(
        Order,
        related_name="lines",
        on_delete=models.CASCADE,
        verbose_name="Užsakymas"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name="Paslauga"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Kiekis"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="laukiama",
        verbose_name="Paslaugos statusas"
    )

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymo eilutės"

    def line_sum(self):
        return self.quantity * self.service.price

    def __str__(self):
        return f"{self.service.name} × {self.quantity}"
