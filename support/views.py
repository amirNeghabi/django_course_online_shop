# support/views.py
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket, TicketMessage
from .forms import TicketCreateForm, TicketMessageForm
from django.urls import reverse_lazy

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketCreateForm
    template_name = 'support/ticket_create.html'
    success_url = reverse_lazy('support:my_tickets')  # ✅ درست

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        # پیام اولیه را ایجاد می‌کنیم
        TicketMessage.objects.create(
            ticket=self.object,
            sender=self.request.user,
            message=form.cleaned_data['message']
        )
        return response


class MyTicketsListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'support/my_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'support/ticket_detail.html'
    context_object_name = 'ticket'

    def get_queryset(self):
        # امنیت: فقط تیکت خود کاربر
        return Ticket.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        # ارسال پیام جدید توسط کاربر
        ticket = self.get_object()
        form = TicketMessageForm(request.POST)
        if form.is_valid():
            TicketMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                message=form.cleaned_data['message']
            )
        return redirect('support:ticket_detail', pk=ticket.pk)
