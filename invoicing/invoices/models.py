from tabnanny import verbose
from uuid import uuid4
from datetime import timedelta
from decimal import Decimal

from errno import EAFNOSUPPORT
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


def get_invoice_number():
    """Auto-generate an invoice number."""
    return 'INV-' + str(uuid4()).split('-')[0]


class Invoice(models.Model):
    """Represents an invoice built and managed by the application."""

    class Terms(models.IntegerChoices):
        TWO_WEEKS = 14, _('14 days')
        ONE_MONTH = 30, _('30 days')
        TWO_MONTH = 60, _('60 days')

    class Currencies(models.TextChoices):
        EUROS = '€', _('EUR')
        SWISS_FRANCS = 'C', _('CHF')
        DOLLARS = '$', _('USD')

    class Statuses(models.IntegerChoices):
        CURRENT = 1, _('Current')
        EMAIL_SENT = 2, _('Email sent')
        OVERDUE = 3, _('Overdue')
        PAID = 4, _('Paid')

    title = models.CharField(
        _('title'),
        blank=True,
        max_length=100,
    )
    number = models.CharField(
        _('number'),
        blank=True,
        max_length=100,
        unique=True,
        default=get_invoice_number,
    )
    payment_term = models.IntegerField(
        _('payment term'),
        choices=Terms.choices,
        blank=True,
        default=Terms.ONE_MONTH,
    )
    due_date = models.DateField(_('due date'), null=True, blank=True)
    currency = models.CharField(
        _('currency'),
        choices=Currencies.choices,
        default=Currencies.EUROS,
        max_length=1,
        blank=True,
    )
    amount_vat = models.DecimalField(
        _('amount vat'),
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=4,
    )
    exemption_vat = models.BooleanField(
        _('exemption vat'),
        default=False,
        max_length=100,
    )
    notes = models.TextField(_('notes'), null=True, blank=True)
    status = models.IntegerField(
        _('status'),
        choices=Statuses.choices,
        default=Statuses.CURRENT,
        blank=True,
    )

    client = models.ForeignKey(
        'clients.Client',
        verbose_name=_('client'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='invoices',
    )

    products = models.ManyToManyField(
        'products.Product',
        related_name='invoices',
        through='InvoiceLine',
    )

    # Utility
    slug = models.SlugField(
        _('slug'),
        max_length=100,
        unique=True,
        blank=True,
        null=True,
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
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    def __str__(self):
        return f'{self.number} - {self.last_updated.strftime("%d %B %Y")}{f" - {self.title}" if self.title else ""}'

    def get_absolute_url(self):
        return reverse('invoices:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.number}')
        super().save(*args, **kwargs)
        self.due_date = self.last_updated + timedelta(days=self.payment_term)
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        total = Decimal("0.0")
        for invoice_line in self.invoice_lines.all():
            total += invoice_line.total_price
        return total


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(
        'Invoice',
        verbose_name=_('invoice'),
        on_delete=models.CASCADE,
        related_name='invoice_lines',
    )
    product = models.ForeignKey(
        'products.Product',
        verbose_name=_('product'),
        on_delete=models.CASCADE,
        related_name='invoice_lines',
    )
    quantity = models.IntegerField(
        _('quantity'),
        null=True,
        blank=True,
        default=1,
    )

    date_created = models.DateTimeField(
        _('date of addition'),
        auto_now_add=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('invoice line')
        verbose_name_plural = _('invoice lines')

    @property
    def price(self):
        prices = self.product.prices.filter(
            currency=self.invoice.currency, date_created__lt=self.date_created
        )
        if prices:
            return prices.first()
        return None

    @property
    def total_price(self):
        if self.price is not None and self.quantity is not None:
            return self.quantity * self.price.value
        return Decimal('0.0')
