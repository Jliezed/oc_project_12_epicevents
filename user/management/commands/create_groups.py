from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from appepicevents.models import Customer, Event, Contract
from user.models import CustomUser


class Command(BaseCommand):
    help = 'Creates a new group with the given name and permissions'

    def handle(self, *args, **kwargs):

        # Create custom groups
        management_group, created = Group.objects.get_or_create(name="Management Group")
        sales_group, created = Group.objects.get_or_create(name="Sales Group")
        support_group, created = Group.objects.get_or_create(name="Support Group")

        # Retrieve full permissions for models
        customer_content_type = ContentType.objects.get_for_model(Customer)
        customer_full_permissions = Permission.objects.filter(
            content_type=customer_content_type)
        contract_content_type = ContentType.objects.get_for_model(Contract)
        contract_full_permissions = Permission.objects.filter(
            content_type=contract_content_type)
        event_content_type = ContentType.objects.get_for_model(Event)
        event_full_permissions = Permission.objects.filter(
            content_type=event_content_type)
        user_content_type = ContentType.objects.get_for_model(CustomUser)
        user_full_permissions = Permission.objects.filter(
            content_type=user_content_type)

        management_permissions = []
        sales_permissions = []
        support_permissions = []

        # Define permissions for Customer Model
        for perm in customer_full_permissions:
            if perm.codename == "add_customer":
                sales_permissions.append(perm)
            elif perm.codename == "change_customer":
                management_permissions.append(perm)
                sales_permissions.append(perm)
            elif perm.codename == "delete_customer":
                sales_permissions.append(perm)
            else:
                management_permissions.append(perm)
                sales_permissions.append(perm)
                support_permissions.append(perm)

        # Define permissions for Contract Model
        for perm in contract_full_permissions:
            if perm.codename == "add_contract":
                sales_permissions.append(perm)
            elif perm.codename == "change_contract":
                management_permissions.append(perm)
                sales_permissions.append(perm)
            elif perm.codename == "delete_contract":
                sales_permissions.append(perm)
            else:
                management_permissions.append(perm)
                sales_permissions.append(perm)
                support_permissions.append(perm)

        # Define permissions for Event Model
        for perm in event_full_permissions:
            if perm.codename == "add_event":
                sales_permissions.append(perm)
            elif perm.codename == "delete_event":
                sales_permissions.append(perm)
            else:
                management_permissions.append(perm)
                sales_permissions.append(perm)
                support_permissions.append(perm)

        # Set permissions for each group
        management_group.permissions.set(management_permissions)
        sales_group.permissions.set(sales_permissions)
        support_group.permissions.set(support_permissions)

        self.stdout.write(
            f'Assigned permissions {management_permissions} to group "{management_group}"')
        self.stdout.write(
            f'Assigned permissions {sales_permissions} to group "{sales_group}"')
        self.stdout.write(
            f'Assigned permissions {support_group} to group "{support_permissions}"')
