from django.db import models
from django.conf import settings


class Customer(models.Model):
    """ Customer Object """

    CUSTOMER_TYPE_CHOICES = (
        ("existing", "Existing"),
        ("prospect", "Prospect"),
    )

    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=250)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES,
                                     default="prospect")

    def __str__(self):
        return self.first_name + " " + self.last_name


class Contract(models.Model):
    """ Contract Object """
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(to=Customer, on_delete=models.DO_NOTHING)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateField()

    def __str__(self):
        return self.customer.company_name


class Event(models.Model):
    """ Event Object """
    EVENT_STATUS_CHOICES = (
        (1, "to come"),
        (2, "done"),
    )

    customer = models.ForeignKey(to=Customer, on_delete=models.DO_NOTHING)
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                        on_delete=models.DO_NOTHING)
    event_status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES)
    attendees = models.IntegerField()
    note = models.TextField(blank=True)
    event_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
