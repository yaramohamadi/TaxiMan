from django import forms
from django.db.models import query
from .models import City


class driver_sign_in(forms.Form):
    username = forms.CharField(label='USERNAME', max_length=100, widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-sand'}))
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class' : 'w3-input w3-border w3-sand'}))

class driver_sign_up(forms.Form):
    username = forms.CharField(label='USERNAME', max_length=100,widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-sand'}))
    email = forms.CharField(label='EMAIL', max_length=100, widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    first_name = forms.CharField(label='FIRST NAME', widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    last_name = forms.CharField(label='LAST NAME', widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    car_model = forms.CharField(label='CAR MODEL', widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    car_plate = forms.CharField(label='CAR PLATE', widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    samples = City.objects.values_list('city_name', flat=True)
    sample_tuple = [(i, i) for i in samples]
    city = forms.ChoiceField(choices=sample_tuple)


class customer_sign_in(forms.Form):
    username = forms.CharField(label='USERNAME', max_length=100,widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-sand'}))
    password = forms.CharField(label='PASSWORD',widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border w3-sand'}))

class customer_sign_up(forms.Form):
    username = forms.CharField(label='USERNAME', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-sand'}))
    email = forms.CharField(label='EMAIL', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-sand'}))
    password = forms.CharField(label='PASSWORD',
                               widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border w3-sand'}))
    first_name = forms.CharField(label='FIRST NAME',
                                 widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-sand'}))
    last_name = forms.CharField(label='LAST NAME',
                                widget=forms.TextInput(attrs={'class': 'w3-input w3-border w3-sand'}))
    samples = City.objects.values_list('city_name', flat=True)
    sample_tuple = [(i, i) for i in samples]
    city = forms.ChoiceField(choices=sample_tuple)


