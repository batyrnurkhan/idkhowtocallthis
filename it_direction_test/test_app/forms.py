from django import forms
from .models import Question, HollandQuestion, UserData


class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['first_name', 'last_name', 'phone_number', 'gender']
