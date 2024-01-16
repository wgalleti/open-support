from django.db import models

from core.mixins import TimeModelMixin, UserModelMixin
from core.models import User


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.username, filename)


class Attachment(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to='core.User',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    @property
    def name(self):
        return str(self.file).split('/')[-1]

    def __str__(self):
        return f'{self.pk}'


class Ticket(TimeModelMixin, UserModelMixin):
    # STATUS
    STATED = 'STATED'
    WORKING = 'WORKING'
    MORE_INFORMATION = 'MORE_INFORMATION'
    WAITING_CUSTOMER = 'WAITING_CUSTOMER'
    NEXT_VERSION = 'NEXT_VERSION'
    SOLVED = 'SOLVED'
    DEPLOYED = 'DEPLOYED'

    # DEPARTMENT
    SUPPORT = 'SUPPORT'
    COMMERCIAL = 'COMMERCIAL'
    DEVELOPMENT = 'DEVELOPMENT'
    FINANCIAL = 'FINANCIAL'

    # Priority
    NORMAL = 'NORMAL'
    HIGH = 'HIGH'

    STATUS = (
        (STATED, 'Started'),
        (WORKING, 'Working'),
        (MORE_INFORMATION, 'More Information'),
        (WAITING_CUSTOMER, 'Waiting Customer'),
        (NEXT_VERSION, 'In the next version'),
        (SOLVED, 'Solved'),
        (DEPLOYED, 'Deployed'),
    )

    DEPARTMENTS = (
        (SUPPORT, 'Support'),
        (COMMERCIAL, 'Commercial'),
        (DEVELOPMENT, 'Development'),
        (FINANCIAL, 'Financial'),
    )

    PRIORITIES = (
        (NORMAL, 'Normal'),
        (HIGH, 'High'),
    )
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE)

    started_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=50, choices=PRIORITIES, default=NORMAL)
    attendant = models.ForeignKey('core.Attendant', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default=STATED)
    departament = models.CharField(max_length=50, choices=DEPARTMENTS, default=SUPPORT)
    files = models.ManyToManyField(
        to='tickets.Attachment',
        blank=True
    )
    version = models.CharField(max_length=50, null=True, blank=True)
    level = models.IntegerField(default=User.LEVEL1, choices=User.LEVELS)
    service_order = models.ForeignKey('services.ServiceOrder', on_delete=models.DO_NOTHING, null=True, blank=True,)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class TicketInteraction(TimeModelMixin, UserModelMixin):
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE)
    attendant = models.ForeignKey('core.Attendant', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    description = models.TextField()
    is_internal = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=Ticket.STATUS, default=Ticket.WORKING)
    departament = models.CharField(max_length=50, choices=Ticket.DEPARTMENTS, default=Ticket.SUPPORT)
    files = models.ManyToManyField(
        to='tickets.Attachment',
        blank=True
    )

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'Ticket Interaction'
        verbose_name_plural = 'Interation of Tickets'
        ordering = ('id',)
