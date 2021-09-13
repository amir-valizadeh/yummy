from django.db import models, transaction
from django.utils.translation import gettext as _
from accounts.models import Customer
from address.models import CustomerAddress
from cart.models import Cart
from gateway.models import Gateway
from library.models import BaseModel
import uuid


class Invoice(BaseModel):
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), related_name='invoices',
                                 on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(verbose_name=_('price'))
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)
    cart = models.OneToOneField(Cart, verbose_name=_('cart'), related_name='invoice', on_delete=models.PROTECT)
    address = models.ForeignKey(CustomerAddress, verbose_name=_('address'), related_name='invoices',
                                on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        db_table = 'invoice'

    @classmethod
    def create_payment(cls, invoice, gateway):
        return Payment.objects.create(invoice=invoice, price=invoice.price, customer=invoice.customer, gateway=gateway)

    @classmethod
    def create(cls, user, cart, address, gateway):
        with transaction.atomic():
            invoice = cls.objects.create(customer=user, cart=cart, price=cart.total_price, address=address)
            payment = cls.create_payment(invoice=invoice, gateway=gateway)

        return payment

    def __str__(self):
        return f"{self.customer} - {self.price} - {'Paid' if self.is_paid else 'Not paid'}"


class Payment(BaseModel):
    uuid = models.UUIDField(unique=True, verbose_name=_('uuid'), db_index=True, default=uuid.uuid4)
    invoice = models.ForeignKey(Invoice, verbose_name=_('invoice'), related_name='payment', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name=_('price'))
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), related_name='payments',
                                 on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)
    gateway = models.ForeignKey(Gateway, verbose_name=_('gateway'), related_name='payments', on_delete=models.SET_NULL,
                                null=True)
    payment_log = models.TextField(verbose_name=_('logs'), blank=True)
    authority = models.CharField(max_length=64, verbose_name=_('authority'), blank=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        db_table = 'payment'

    def __str__(self):
        return f"{self.price} - {'Paid' if self.is_paid else 'Not paid'}"
