# support/urls.py
from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('new/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('my-tickets/', views.MyTicketsListView.as_view(), name='my_tickets'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
]
