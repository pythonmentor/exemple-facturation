from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Product(models.Model):
    """Represents a product invoiced by the user."""

    name = models.CharField(_('name'), max_length=150)
    description = models.TextField(_('description'), blank=True)
    price = models.DecimalField(
        _('unit price'), null=True, blank=True, decimal_places=2, max_digits=8
    )

    # Utility fields
    slug = models.SlugField(
        _('slug'), max_length=500, unique=True, blank=True, null=True
    )
    date_created = models.DateTimeField(
        _('date of creation'),
        auto_now_add=True,
    )
    last_updated = models.DateTimeField(
        _('date of last update'),
        auto_now=True,
    )

    class Meta:
        ordering = ('name', 'id')
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return f'{self.name} - {self.price} EUR'

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
