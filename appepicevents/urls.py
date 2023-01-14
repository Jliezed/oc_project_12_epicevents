from django.urls import path, include

from rest_framework_nested import routers

from appepicevents.views import CustomerViewSet, ContractViewSet, EventViewSet

# Define main route
router = routers.SimpleRouter()
router.register("customers", CustomerViewSet, basename="customers")

# Define nested routes customers/<id>/contracts/<id>/
customers_router = routers.NestedSimpleRouter(router, 'customers', lookup="customer")
customers_router.register('contracts', ContractViewSet, basename="customer-contracts")

# Define nested routes customers/<id>/contracts/<id>/events/<id>
contracts_router = routers.NestedSimpleRouter(customers_router, "contracts",
                                              lookup="contract")
contracts_router.register("events", EventViewSet, basename="contract-events")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(customers_router.urls)),
    path('', include(contracts_router.urls)),
]
