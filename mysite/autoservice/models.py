from django.db import models

class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=200)
    price = models.FloatField(verbose_name="Kaina")

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

    def __str__(self):
        return f"{self.name} ({self.price} €)"


class Car(models.Model):
    make = models.CharField(verbose_name="Markė", max_length=100)
    model = models.CharField(verbose_name="Modelis", max_length=100)
    license_plate = models.CharField(verbose_name="Valstybinis numeris", max_length=20)
    vin_code = models.CharField(verbose_name="VIN kodas", max_length=50)
    client_name = models.CharField(verbose_name="Klientas", max_length=200)

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class Order(models.Model):
    date = models.DateField(verbose_name="Data")
    car = models.ForeignKey("Car", verbose_name="Automobilis", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"

    def __str__(self):
        return f"Užsakymas #{self.id} – {self.car}"


class OrderLine(models.Model):
    order = models.ForeignKey("Order", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey("Service", verbose_name="Paslauga", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Kiekis")

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymo eilutės"

    def __str__(self):
        return f"{self.service.name} x {self.quantity}"
