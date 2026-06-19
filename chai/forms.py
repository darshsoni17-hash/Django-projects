from django import forms
from .models import chaivarity


class chaivarityForm(forms.Form):
    chai_varity = forms.ModelChoiceField(
        queryset=chaivarity.objects.all(),
        empty_label='Select a chai')
    

