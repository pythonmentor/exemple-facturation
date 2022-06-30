from django.contrib import admin

from .models import Invoice, InvoiceLine

admin.site.register(InvoiceLine)


class InvoiceLineInline(admin.StackedInline):
    model = InvoiceLine
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = (InvoiceLineInline,)
    list_display = ('number', 'title', 'last_updated')
