from django.contrib import admin

from appepicevents.models import Customer, Contract, Event


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Search & Filter
    search_fields = [
        "first_name",
        "last_name",
        "email",
    ]

    list_filter = ('email', 'company_name', 'sales_contact',)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    # List page
    list_display = ('customer', 'status', 'sales_contact')

    # Search & Filter
    search_fields = [
        "customer",
        "status",
    ]

    list_filter = ('customer', 'status', 'sales_contact',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # List page
    list_display = ('customer', 'event_status', 'support_contact')

    # Search & Filter
    search_fields = [
        "customer",
        "support_contact",
        "event_status",
        "event_date",
    ]

    list_filter = ('customer', 'event_status', 'support_contact', 'note',
                   'attendees', 'event_date',)
