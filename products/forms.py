from django import forms
from products import models
from django.db.models import fields


CHART_CHOICES = (
    ("#1", "BAR CAHRT"),
    ("#2", "PIE CHART"),
    ("#3", "LINE CHART")
)

class product_form(forms.ModelForm):
    class Meta():

        model = models.Product_Model
        fields = ("name", "image", "price", "bio")

class prod_comm(forms.ModelForm):
    class Meta():
        model = models.product_comment
        fields = ('body',)
        
class order_search(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)


class sales_search(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
