from django.contrib import admin

from .models import Product, Price

admin.site.register(Price)


class PriceInline(admin.StackedInline):
    model = Price
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (PriceInline,)
    readonly_fields = ('id',)
    list_display = ('name', 'date_created', 'last_updated')
    prepopulated_fields = {
        'slug': ('name',),
    }
