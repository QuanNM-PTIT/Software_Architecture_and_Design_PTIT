from django.urls import path
from .views import OrderItemListView, OrderListByStatus, AddToOrderView, OrderItemView

urlpatterns = [
    path('all/', OrderItemListView.as_view(), name='order_item_list'),
    path('order_items/status/', OrderListByStatus.as_view(), name='order_list_by_status'),
    path('order_items/add/', AddToOrderView.as_view(), name='add_to_order'),
    path('order_items/view/', OrderItemView.as_view(), name='order_item_view'),
]
