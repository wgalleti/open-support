from core.mixins import TimeModelMixin, UserModelMixin
from django.db import models


class ServiceType(TimeModelMixin, UserModelMixin):
    description = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Service Type"
        verbose_name_plural = "Types of Services"


class Service(TimeModelMixin, UserModelMixin):
    description = models.CharField(max_length=100)
    erp_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class ServiceOrder(TimeModelMixin, UserModelMixin):
    STARTED = 1
    RUNNING = 2
    FINISHED = 3
    CANCELED = 9

    STATUS = (
        (STARTED, "Started"),
        (RUNNING, "Running"),
        (FINISHED, "Finished"),
        (CANCELED, "Canceled"),
    )

    date = models.DateField()
    closure_date = models.DateField(null=True, blank=True)
    closure_user = models.ForeignKey(
        "core.User",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="user_closure",
    )

    cancellation_date = models.DateField(null=True, blank=True)
    cancellation_user = models.ForeignKey(
        "core.User",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="user_cancellation",
    )
    cancellation_description = models.TextField(null=True, blank=True)

    status = models.IntegerField(default=STARTED, choices=STATUS)
    customer = models.ForeignKey("core.Customer", on_delete=models.DO_NOTHING)
    description = models.TextField()
    observation = models.TextField(null=True, blank=True)
    discount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, null=True, blank=True
    )
    integration_create = models.BooleanField(default=True, null=True, blank=True)

    @property
    def value(self):
        values = sum(i.value for i in self.ordemservicoitem_set.all())
        return values - self.discount

    @property
    def provided_value(self):
        values = sum(i.value for i in self.ordemservicotecnico_set.all())
        return values

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Service Order"
        verbose_name_plural = "Services Orders"


class ServiceOrderItem(TimeModelMixin, UserModelMixin):
    service_order = models.ForeignKey("services.ServiceOrder", on_delete=models.CASCADE)
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    duration = models.IntegerField(default=1, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Service Order Item"
        verbose_name_plural = "Items of Services Orders"


class ServiceOrderTech(TimeModelMixin, UserModelMixin):
    service_order = models.ForeignKey("services.ServiceOrder", on_delete=models.CASCADE)
    service_type = models.ForeignKey(
        "services.ServiceType", on_delete=models.DO_NOTHING
    )
    tech = models.ForeignKey("core.Attendant", on_delete=models.DO_NOTHING)
    duration = models.IntegerField()
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.pk} - {self.tech}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save()
        self.service_order.status = ServiceOrder.RUNNING
        self.service_order.save()

    class Meta:
        verbose_name = "Service Order Tech"
        verbose_name_plural = "Techs of Services Orders"
