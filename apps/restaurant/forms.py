from django import forms
from django.forms import widgets

from apps.restaurant.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('date', 'name', 'email', 'table', 'hall')
        widgets = {
            'hall': widgets.HiddenInput(),
        }
