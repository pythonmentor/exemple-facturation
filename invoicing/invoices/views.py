from django.views.generic import TemplateView


class InvoiceListView(TemplateView):
    template_name = "invoices/list.html"
