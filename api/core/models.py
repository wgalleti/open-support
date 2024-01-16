from django.contrib.auth.models import AbstractUser
from django.db import models


class MailError(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    log = models.TextField()
    smtp = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.log


class User(AbstractUser):
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3

    LEVELS = (
        (LEVEL1, "Support 1"),
        (LEVEL2, "Support 2"),
        (LEVEL3, "Support 3"),
    )

    is_attendant = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="profiles/", null=True, blank=True)
    level = models.IntegerField(default=LEVEL1, choices=LEVELS)


class Attendant(models.Model):
    access_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    level = models.IntegerField(default=User.LEVEL1, choices=User.LEVELS)
    active = models.BooleanField(default=True)

    hourly_cost_value = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, null=True, blank=True
    )
    hourly_sell_value = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Attendant"
        verbose_name_plural = "Attendants"


class Customer(models.Model):
    customer_code = models.IntegerField(blank=True, null=True)
    access_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    app_version = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.customer_code}-{self.name}"

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class CustomerUpdate(models.Model):
    customer = models.ForeignKey("core.Customer", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = "Customer Update"
        verbose_name_plural = "Customers Updates"


class CustomerGroup(models.Model):
    name = models.CharField(max_length=100)
    customers = models.ManyToManyField(
        "core.Customer",
        blank=True,
    )

    @property
    def count(self):
        return len(self.customers.all())

    def __str__(self):
        return self.name
