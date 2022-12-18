from django.db.models import fields
from order.models import Order
from django import forms


CHOICES=[  ('Semi Cash On Delivery', 'Semi Cash On Delivery'),
        ('RazorPay', 'RazorPay'),]
class PaymentMethodForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=CHOICES,  widget=forms.RadioSelect(attrs={'class': 'checkbox_item mb_15 pl-0'}))
    class Meta:
        model = Order
        fields = ['payment_method',]