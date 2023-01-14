from rest_framework.serializers import ModelSerializer, SlugRelatedField, \
    HyperlinkedIdentityField, StringRelatedField
from django.contrib.auth import get_user_model

from appepicevents.models import Customer, Contract, Event


class CustomerSerializer(ModelSerializer):
    """ Serializer for Customer Model """
    edit_url = HyperlinkedIdentityField(view_name="customers-detail")
    sales_contact = SlugRelatedField(queryset=get_user_model().objects.all(),
                                     slug_field="username")

    class Meta:
        model = Customer
        fields = [
            "id",
            "edit_url",
            "sales_contact",
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobile",
            "company_name",
            "date_created",
            "date_updated",
            "customer_type",
        ]


class ContractSerializer(ModelSerializer):
    """ Serializers for Contract Model """
    sales_contact = StringRelatedField(read_only=True)
    customer = StringRelatedField(read_only=True)

    class Meta:
        model = Contract
        fields = [
            "id",
            "sales_contact",
            "customer",
            "date_created",
            "date_updated",
            "status",
            "amount",
            "payment_due",
        ]


class EventSerializer(ModelSerializer):
    """ Serializer for Event Model """
    customer = StringRelatedField(read_only=True)
    support_contact = SlugRelatedField(queryset=get_user_model().objects.all(),
                                       slug_field="username")

    class Meta:
        model = Event
        fields = [
            "id",
            "customer",
            "support_contact",
            "event_status",
            "attendees",
            "note",
            "event_date",
            "date_created",
            "date_updated",
        ]
