from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, HollandQuestion, PreferenceQuestion, CareerAnchorQuestion, UserData, TestResult
from .forms import UserDataForm, SurveyForm, CareerAnchorForm

def collect_user_data_view(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            user_data = form.save()
            return redirect('test_view', user_data_id=user_data.id)
    else:
        form = UserDataForm()
    return render(request, 'test_app/userform.html', {'form': form})

def test_view(request, user_data_id):
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
        TestResult.objects.create(user_data_id=user_data_id, test_name="General Test", result=result)
        return render(request, 'test_app/results.html', {'result': result, 'user_data_id': user_data_id})
    else:
        questions = Question.objects.all()
        return render(request, 'test_app/test.html', {'questions': questions, 'user_data_id': user_data_id})

def holland_test(request, user_data_id):
    if request.method == 'POST':
        responses = request.POST.dict()
        type_keys = {
            'Реалистический тип': ['1а', '2а', '3а', '4а', '5а', '16а', '17а', '18а', '19а', '21а', '31а', '32а', '33а', '34а'],
            'Интеллектуальный тип': ['1б', '6а', '7а', '8а', '9а', '16б', '20а', '22а', '23а', '24а', '31б', '35а', '36а', '37а'],
            'Социальный тип': ['2б', '6б', '10а', '11а', '12а', '17б', '29б', '25а', '26а', '27а', '36б', '38а', '39а', '41б'],
            'Конвенциональный тип': ['3б', '7б', '10б', '13а', '14а', '18б', '22б', '25б', '28а', '29а', '32б', '38б', '40а', '42а'],
            'Предприимчивый тип': ['4б', '8б', '11б', '13б', '15а', '23б', '28б', '30а', '33б', '35б', '37б', '39б', '40б'],
            'Артистический тип': ['5б', '9б', '12б', '14б', '15б', '19б', '21б', '24а', '27б', '29б', '30б', '34б', '41а', '42б']
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
        TestResult.objects.create(user_data_id=user_data_id, test_name="Holland Test", result=max_type)
        return render(request, 'test_app/result_template.html', {'result': max_type, 'user_data_id': user_data_id})
    else:
        questions = HollandQuestion.objects.all()
        return render(request, 'test_app/holland_test_template.html', {'questions': questions, 'user_data_id': user_data_id})

def preference_test_view(request, user_data_id):
    if request.method == 'POST':
        scores = {
            'work_with_people': 0,
            'intellectual_work': 0,
            'technical_interests': 0,
            'aesthetics_and_art': 0,
            'physical_work': 0,
            'material_interests': 0,
        }

        question_category_map = {
            '2a': 'work_with_people', '4a': 'work_with_people', '6b': 'work_with_people', '9a': 'work_with_people', '12b': 'work_with_people',
            '16a': 'work_with_people', '17b': 'work_with_people', '19b': 'work_with_people', '23b': 'work_with_people', '28b': 'work_with_people',
            '4b': 'intellectual_work', '7a': 'intellectual_work', '10b': 'intellectual_work', '13a': 'intellectual_work', '14b': 'intellectual_work',
            '18a': 'intellectual_work', '20a': 'intellectual_work', '21b': 'intellectual_work', '26b': 'intellectual_work', '30a': 'intellectual_work',
            '1b': 'technical_interests', '3b': 'technical_interests', '6a': 'technical_interests', '8b': 'technical_interests', '12a': 'technical_interests',
            '14a': 'technical_interests', '15b': 'technical_interests', '25a': 'technical_interests', '26a': 'technical_interests', '29b': 'technical_interests',
            '1a': 'aesthetics_and_art', '5b': 'aesthetics_and_art', '8a': 'aesthetics_and_art', '10a': 'aesthetics_and_art', '11b': 'aesthetics_and_art',
            '17a': 'aesthetics_and_art', '21a': 'aesthetics_and_art', '23a': 'aesthetics_and_art', '24b': 'aesthetics_and_art', '28a': 'aesthetics_and_art',
            '2b': 'physical_work', '5a': 'physical_work', '13b': 'physical_work', '15a': 'physical_work', '18b': 'physical_work',
            '20b': 'physical_work', '22a': 'physical_work', '24a': 'physical_work', '25b': 'physical_work', '27a': 'physical_work',
            '3a': 'material_interests', '7b': 'material_interests', '9b': 'material_interests', '11a': 'material_interests', '16b': 'material_interests',
            '19a': 'material_interests', '22b': 'material_interests', '27b': 'material_interests', '29a': 'material_interests', '30b': 'material_interests',
        }

        for key, value in request.POST.items():
            if key.startswith('question'):
                question_id, option = key.split('_')[1], value[-1]  # Assuming the last character is the option (a/b)
                score = int(value[:-1])  # Assuming the score is everything except the last character
                category = question_category_map.get(f'{question_id}{option}')
                if category:
                    scores[category] += score

        preferred_category = max(scores, key=scores.get)
        TestResult.objects.create(user_data_id=user_data_id, test_name="Preference Test", result=preferred_category)
        return render(request, 'test_app/preference_result.html', {'preferred_category': preferred_category, 'user_data_id': user_data_id})
    else:
        questions = PreferenceQuestion.objects.all()
        return render(request, 'test_app/preference_test.html', {'questions': questions, 'user_data_id': user_data_id})

def survey_view(request, user_data_id):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            answers = form.cleaned_data
            results = answers.values()

            # Инициализация списка результатов для каждой категории
            results_by_category = [0] * 29
            levels_mapping = {
                -12: "высшая степень отрицания данного интереса",
                -11: "высшая степень отрицания данного интереса",
                -10: "высшая степень отрицания данного интереса",
                -9: "высшая степень отрицания данного интереса",
                -8: "высшая степень отрицания данного интереса",
                -7: "выраженный интерес",
                -6: "выраженный интерес",
                -5: "выраженный интерес",
                -4: "интерес выражен слабо",
                -3: "интерес выражен слабо",
                -2: "интерес выражен слабо",
                -1: "интерес выражен слабо",
                0: "интерес отрицается",
                1: "интерес выражен слабо",
                2: "интерес выражен слабо",
                3: "интерес выражен слабо",
                4: "интерес выражен слабо",
                5: "выраженный интерес",
                6: "выраженный интерес",
                7: "выраженный интерес",
                8: "ярко выраженный интерес",
                9: "ярко выраженный интерес",
                10: "ярко выраженный интерес",
                11: "ярко выраженный интерес",
                12: "ярко выраженный интерес",
            }

            # Определение значений для каждой переменной в зависимости от ответов
            for i, result in enumerate(results, start=1):
                question_index = (i - 1) % 29  # Вычисляем индекс вопроса от 0 до 28 для каждого i
                if result == '++':
                    results_by_category[question_index] += 2
                elif result == '+':
                    results_by_category[question_index] += 1
                elif result == '-':
                    results_by_category[question_index] -= 1
                elif result == '--':
                    results_by_category[question_index] -= 2
                else:
                    pass  # Ничего не делаем, если ответ не указан

            categories = {
                "Биология": levels_mapping.get(results_by_category[0], "Недопустимое значение"),
                "География": levels_mapping.get(results_by_category[1], "Недопустимое значение"),
                "Геология": levels_mapping.get(results_by_category[2], "Недопустимое значение"),
                "Медицина": levels_mapping.get(results_by_category[3], "Недопустимое значение"),
                "Легкая и пищевая промышленность": levels_mapping.get(results_by_category[4], "Недопустимое значение"),
                "Физика": levels_mapping.get(results_by_category[5], "Недопустимое значение"),
                "Химия": levels_mapping.get(results_by_category[6], "Недопустимое значение"),
                "Техника": levels_mapping.get(results_by_category[7], "Недопустимое значение"),
                "Электро- и радиотехника": levels_mapping.get(results_by_category[8], "Недопустимое значение"),
                "Металлообработка": levels_mapping.get(results_by_category[9], "Недопустимое значение"),
                "Деревообработка": levels_mapping.get(results_by_category[10], "Недопустимое значение"),
                "Строительство": levels_mapping.get(results_by_category[11], "Недопустимое значение"),
                "Транспорт": levels_mapping.get(results_by_category[12], "Недопустимое значение"),
                "Авиация, морское дело": levels_mapping.get(results_by_category[13], "Недопустимое значение"),
                "Военные специальности": levels_mapping.get(results_by_category[14], "Недопустимое значение"),
                "История": levels_mapping.get(results_by_category[15], "Недопустимое значение"),
                "Литература": levels_mapping.get(results_by_category[16], "Недопустимое значение"),
                "Журналистика": levels_mapping.get(results_by_category[17], "Недопустимое значение"),
                "Общественная деятельность": levels_mapping.get(results_by_category[18], "Недопустимое значение"),
                "Педагогика": levels_mapping.get(results_by_category[19], "Недопустимое значение"),
                "Юриспруденция": levels_mapping.get(results_by_category[20], "Недопустимое значение"),
                "Сфера обслуживания": levels_mapping.get(results_by_category[21], "Недопустимое значение"),
                "Математика": levels_mapping.get(results_by_category[22], "Недопустимое значение"),
                "Экономика": levels_mapping.get(results_by_category[23], "Недопустимое значение"),
                "Иностранные языки": levels_mapping.get(results_by_category[24], "Недопустимое значение"),
                "Изобразительное искусство": levels_mapping.get(results_by_category[25], "Недопустимое значение"),
                "Сценическое искусство": levels_mapping.get(results_by_category[26], "Недопустимое значение"),
                "Музыка": levels_mapping.get(results_by_category[27], "Недопустимое значение"),
                "Физкультура и спорт": levels_mapping.get(results_by_category[28], "Недопустимое значение")
            }
            print(categories)



            results = {'++': 0, '+': 0, '0': 0, '-': 0, '--': 0}

            for answer in answers.values():
                results[answer] += 1
            # Здесь можно сделать что-то с results, например, передать их в шаблон
            TestResult.objects.create(user_data_id=user_data_id, test_name="Survey", result=categories)
            return render(request, 'test_app/survey_result.html', {'categories': categories, 'user_data_id': user_data_id})
    else:
        form = SurveyForm()

    return render(request, 'test_app/survey_test.html', {'form': form})




from django.shortcuts import render
from .forms import CareerAnchorForm
from .models import CareerAnchorQuestion


def career_anchor_test_view(request, user_data_id):
    form = CareerAnchorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        career_orientations_scores = {
            'Профессиональная компетентность': 0,
            'Менеджмент': 0,
            'Автономия (независимость)': 0,
            'Стабильность работы': 0,
            'Стабильность места жительства': 0,
            'Служение': 0,
            'Вызов': 0,
            'Интеграция стилей жизни': 0,
            'Предпринимательство': 0,
        }
        question_orientations_mapping = {
            'Профессиональная компетентность': [1, 9, 17, 25, 33],
            'Менеджмент': [2, 10, 18, 26, 34],
            'Автономия (независимость)': [3, 11, 19, 27, 35],
            'Стабильность работы': [4, 12, 36],
            'Стабильность места жительства': [20, 28, 41],
            'Служение': [5, 13, 21, 29, 37],
            'Вызов': [6, 14, 22, 30, 38],
            'Интеграция стилей жизни': [7, 15, 23, 31, 39],
            'Предпринимательство': [8, 16, 24, 32, 40],
        }
        for question_id, score in form.cleaned_data.items():
            q_id = int(question_id.split('_')[1])
            score = int(score)
            for orientation, questions in question_orientations_mapping.items():
                if q_id in questions:
                    career_orientations_scores[orientation] += score
                    break
        max_orientation = max(career_orientations_scores, key=career_orientations_scores.get)
        TestResult.objects.create(user_data_id=user_data_id, test_name="Career Anchor Test", result=max_orientation)
        return render(request, 'test_app/career_anchor_results.html', {
            'max_orientation': max_orientation,
            'user_data_id': user_data_id
        })

    return render(request, 'test_app/career_anchor_test.html', {
        'form': form,
        'user_data_id': user_data_id
    })