from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import Question
from .forms import HollandQuestion, UserDataForm

def test_view(request):
    if request.method == 'POST':
        profession_groups_count = {
            'Human-Nature': 0,
            'Human-Technique': 0,
            'Human-Human': 0,
            'Human-Sign Systems': 0,
            'Human-Artistic Image': 0
        }
        for key, value in request.POST.items():
            if key.startswith('question'):
                profession_groups_count[value] += 1

        result = max(profession_groups_count, key=profession_groups_count.get)
        return render(request, 'test_app/results.html', {'result': result})
    else:
        questions = Question.objects.all()
        return render(request, 'test_app/test.html', {'questions': questions})

def holland_test(request):
    if request.method == 'POST':
        responses = request.POST.dict()
        type_keys = {
            'Реалистический тип': ['1а', '2а', '3а', '4а', '5а', '16а', '17а', '18а', '19а', '21а', '31а', '32а', '33а',
                                   '34а'],
            'Интеллектуальный тип': ['1б', '6а', '7а', '8а', '9а', '16б', '20а', '22а', '23а', '24а', '31б', '35а',
                                     '36а', '37а'],
            'Социальный тип': ['2б', '6б', '10а', '11а', '12а', '17б', '29б', '25а', '26а', '27а', '36б', '38а', '39а',
                               '41б'],
            'Конвенциональный тип': ['3б', '7б', '10б', '13а', '14а', '18б', '22б', '25б', '28а', '29а', '32б', '38б',
                                     '40а', '42а'],
            'Предприимчивый тип': ['4б', '8б', '11б', '13б', '15а', '23б', '28б', '30а', '33б', '35б', '37б', '39б',
                                   '40б'],
            'Артистический тип': ['5б', '9б', '12б', '14б', '15б', '19б', '21б', '24а', '27б', '29б', '30б', '34б',
                                  '41а', '42б']
        }

        type_counts = {type_key: 0 for type_key in type_keys}

        for question_id, choice_selected in responses.items():
            if choice_selected == 'a':
                choice_selected = 'а'
            elif choice_selected == 'b':
                choice_selected = 'б'

            for type_key, keys in type_keys.items():
                if question_id in keys and choice_selected == 'а':
                    type_counts[type_key] += 1
                elif question_id in keys and choice_selected == 'б':
                    type_counts[type_key] -= 1

        max_type = max(type_counts, key=type_counts.get)
        return render(request, 'test_app/result_template.html', {'result': max_type})

    else:
        questions = HollandQuestion.objects.all()
        return render(request, 'test_app/holland_test_template.html', {'questions': questions})

class UserDataView(FormView):
    template_name = 'test_app/userdata_form_template.html'
    form_class = UserDataForm
    success_url = reverse_lazy('test_view')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
