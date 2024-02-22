from django import forms

from .models import *

class SurveyForm(forms.Form):
    CHOICES = [
        ('++', 'Очень нравится'),
        ('+', 'Нравится'),
        ('0', 'Не знаю/Сомневаюсь'),
        ('-', 'Не нравится'),
        ('--', 'Очень не нравится')
    ]

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        questions = MapQuestion.objects.all()
        for i, question in enumerate(questions, start=1):
            field_name = f'question_{i}'
            self.fields[field_name] = forms.ChoiceField(choices=self.CHOICES, widget=forms.RadioSelect,
                                                        label=question.text)


from .models import CareerAnchorQuestion

class CareerAnchorForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CareerAnchorForm, self).__init__(*args, **kwargs)
        questions = CareerAnchorQuestion.objects.all()
        for question in questions:
            field_name = f'question_{question.id}'
            choices = [(str(i), str(i)) for i in range(1, 11)]  # Scale from 1 to 10
            self.fields[field_name] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.text)

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['first_name', 'last_name', 'email', 'phone_number']
