from django.views.generic import ListView, DetailView

from .models import Invoice


class InvoiceListView(ListView):
    model = Invoice
    template_name = "invoices/list.html"
    context_object_name = 'invoices'


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = "invoices/detail.html"
    context_object_name = 'invoice'
