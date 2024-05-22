from django.urls import path
from .views import ShipmentCreateView, ShipmentDetailView

urlpatterns = [
    path('shipments/', ShipmentCreateView.as_view(), name='shipment-create'),
    path('shipments/<int:pk>/', ShipmentDetailView.as_view(), name='shipment-detail'),
]
