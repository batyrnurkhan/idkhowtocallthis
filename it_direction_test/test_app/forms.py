from django import forms
from django.shortcuts import render, redirect

from .models import *


CHOICES_RU = [
    ('++', 'Очень нравится'),
    ('+', 'Нравится'),
    ('0', 'Не знаю/Сомневаюсь'),
    ('-', 'Не нравится'),
    ('--', 'Очень не нравится')
]

CHOICES_KZ = [
    ('++', 'Өте ұнайды'),
    ('+', 'Ұнайды'),
    ('0', 'Білмеймін/Күмәнданамын'),
    ('-', 'Ұнамайды'),
    ('--', 'Мүлдем ұнамайды')
]
class SurveyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', 'RU')
        super().__init__(*args, **kwargs)
        self.CHOICES = CHOICES_KZ if language == 'KZ' else CHOICES_RU
        questions = MapQuestion.objects.all()
        for i, question in enumerate(questions, start=1):
            field_name = f'question_{i}'
            self.fields[field_name] = forms.ChoiceField(choices=self.CHOICES, widget=forms.RadioSelect, label=question.text)
class SurveyForm_kk(forms.Form):

    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', 'RU')
        super().__init__(*args, **kwargs)
        self.CHOICES_kz = CHOICES_KZ
        questions = MapQuestion_kk.objects.all()
        for i, question in enumerate(questions, start=1):
            field_name = f'question_{i}'
            self.fields[field_name] = forms.ChoiceField(choices=self.CHOICES_kz, widget=forms.RadioSelect, label=question.text)

from .models import CareerAnchorQuestion

class CareerAnchorForm(forms.Form):
    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', 'RU')
        super().__init__(*args, **kwargs)
        questions = CareerAnchorQuestion.objects.all()
        for question in questions:
            field_name = f'question_{question.id}'
            choices = [(str(i), str(i)) for i in range(1, 11)]
            self.fields[field_name] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.text)
class CareerAnchorForm_kk(forms.Form):
    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', 'RU')
        super().__init__(*args, **kwargs)
        questions = CareerAnchorQuestion_kk.objects.all()
        for question in questions:
            field_name = f'question_{question.id}'
            choices = [(str(i), str(i)) for i in range(1, 11)]
            self.fields[field_name] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.text)
class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'language',
                  'grade', 'parent_first_name', 'parent_last_name', 'parent_phone_number']
