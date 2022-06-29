from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('name', 'price', 'date_created', 'last_updated')
    prepopulated_fields = {
        'slug': ('name',),
    }
