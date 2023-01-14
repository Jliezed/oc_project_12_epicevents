import logging

from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from appepicevents.models import Customer, Contract, Event
from appepicevents.serializers import CustomerSerializer, ContractSerializer, \
    EventSerializer

logger = logging.getLogger(__name__)


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name', 'email', 'company_name']
    search_fields = ['first_name', 'last_name', 'email', 'company_name']
    ordering_fields = ['first_name', 'last_name', 'email', 'company_name']
    ordering = ["company_name"]

    logger.info('Processing request...')

    def perform_update(self, serializer):
        customer = serializer.instance
        if self.request.user.groups.filter(
                name='Sales Group').exists() and customer.sales_contact != \
                self.request.user:
            raise PermissionDenied('You are not allowed to update this customer')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name='Sales Group').exists() and \
                instance.sales_contact != self.request.user:
            raise PermissionDenied('You are not allowed to delete this customer')
        instance.delete()


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['customer', 'sales_contact', 'status']
    search_fields = ['customer', 'sales_contact', 'status']
    ordering_fields = ['customer', 'sales_contact', 'status']
    ordering = ["customer"]

    def get_queryset(self):
        return Contract.objects.filter(customer_id=self.kwargs["customer_pk"])

    def perform_create(self, serializer):
        """ When creating a new contract for customer,
        set automatically customer and sales_contact"""
        customer = get_object_or_404(Customer, pk=self.kwargs["customer_pk"])
        serializer.save(customer=customer, sales_contact=customer.sales_contact)

    def perform_update(self, serializer):
        customer = serializer.instance
        if self.request.user.groups.filter(
                name='Sales Group').exists() and customer.sales_contact != \
                self.request.user:
            raise PermissionDenied('You are not allowed to update this customer')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name='Sales Group').exists() and \
                instance.sales_contact != self.request.user:
            raise PermissionDenied('You are not allowed to delete this customer')
        instance.delete()


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['customer', 'support_contact', 'event_status', 'attendees',
                        'event_date']
    search_fields = ['customer']
    ordering_fields = ['customer']
    ordering = ["customer"]

    def get_queryset(self):
        return Event.objects.filter(customer_id=self.kwargs["customer_pk"])

    def perform_create(self, serializer):
        """ When creating a new event for a specific customer & contract,
        set automatically customer """
        customer = get_object_or_404(Customer, pk=self.kwargs["customer_pk"])
        serializer.save(customer=customer)

    def perform_update(self, serializer):
        event = serializer.instance
        if self.request.user.groups.filter(
                name__in=['Support Group']).exists() and \
                event.support_contact != self.request.user:
            raise PermissionDenied('You are not allowed to update this customer')
        if self.request.user.groups.filter(
                name__in=['Sales Group']).exists() and \
                event.customer.sales_contact != self.request.user:
            raise PermissionDenied('You are not allowed to update this customer')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name='Sales Group').exists() and \
                instance.customer.sales_contact != self.request.user:
            raise PermissionDenied('You are not allowed to delete this customer')
        instance.delete()
