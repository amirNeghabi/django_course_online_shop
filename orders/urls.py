from django.urls import path
from .views import order_create_view, order_list_view, order_detail_view

app_name = 'orders'


urlpatterns = [
    path('create/', order_create_view, name='order_create'),              
    path('my-orders/', order_list_view, name='order_list'),               
    path('my-orders/<int:pk>/', order_detail_view, name='order_detail'),  
]
