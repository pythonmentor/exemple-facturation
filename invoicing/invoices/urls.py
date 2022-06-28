from django.urls import path

from . import views

app_name = "invoices"

urlpatterns = [
    path('', views.InvoiceListView.as_view(), name="list"),
]
