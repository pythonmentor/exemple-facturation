"""
Invoicing URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('invoicing.core.urls')),
    path('invoices/', include('invoicing.invoices.urls')),
]
