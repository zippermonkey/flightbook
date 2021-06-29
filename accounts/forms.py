from django.forms import ModelForm, Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Flight


class FlightForm(ModelForm):

    class Meta:
        model = Flight
        fields = ['name','start','end','departureTime','price']

class MyForm(Form):
    flight_no = forms.CharField(label='航班号', max_length=200)
    start = forms.CharField(label='起点',max_length=200)
    end = forms.CharField(label='到达', max_length=200)
    departureTime = forms.DateTimeField(label='起飞时间')
    price = forms.FloatField(min_value=0)