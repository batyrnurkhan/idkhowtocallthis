from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, HollandQuestion, PreferenceQuestion, CareerAnchorQuestion, UserData, TestResult
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import UserData, TestResult, Question, Question_kk
from urllib.parse import quote


def create_whatsapp_link(domain, admin_change_path, message_text):
    admin_url = f"{domain}{admin_change_path}"
    whatsapp_message = f"{message_text} {admin_url}"
    encoded_whatsapp_message = quote(whatsapp_message)
    return f"https://wa.me/77000660868?text={encoded_whatsapp_message}"


def test(request):
    phone_num = '+77476283763'
    text = "Hello world"
    link = 'https://wa.me/' + phone_num + '?text=' + text.replace(" ", "%20")
    return render(request, 'test_app/test.html', {'link': link})


def index(request, user_data_id):
    user_data = get_object_or_404(UserData, id=user_data_id)
    # Retrieve submit_text from session or set based on user_data.language
    submit_text = request.session.pop('submit_text', 'ПОЛУЧИТЬ РЕЗУЛЬТАТ')  # Pop to clear after use

    if user_data.language == 'KZ':
        template_name = 'test_app/home_kz.html'
    else:
        template_name = 'test_app/home.html'

    return render(request, template_name, {
        'user_data_id': user_data_id,
        'submit_text': submit_text
    })


def collect_user_data_view(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            user_data = form.save()
            # Determine the submit text based on the user's language selection
            if user_data.language == 'KZ':
                request.session['submit_text'] = 'Жіберу'  # Kazakh
            else:
                request.session['submit_text'] = 'ПОЛУЧИТЬ РЕЗУЛЬТАТ'  # Default to Russian
            return redirect('home', user_data_id=user_data.id)

    else:
        form = UserDataForm()

    return render(request, 'test_app/userform.html', {'form': form})


def test_view(request, user_data_id):
    user_data = get_object_or_404(UserData, id=user_data_id)
    language = user_data.language  # Retrieve the user's language preference from the UserData model
    submit_text = "Бастау" if language == "KZ" else "ПОЛУЧИТЬ РЕЗУЛЬТАТ"

    if request.method == 'POST':
        # Your existing logic for processing POST requests remains unchanged
        # Dictionary to hold the counts for each category
        profession_groups_count = {
            'Human-Nature': 0,
            'Human-Technique': 0,
            'Human-Human': 0,
            'Human-Sign Systems': 0,
            'Human-Artistic Image': 0
        }

        # Counter to keep track of the index
        i = 0

        # Iterate through the items in the POST data
        for key, value in request.POST.items():
            i += 1  # Increment the index for each item

            # Check the value and index, then increment the appropriate category count
            if value == "a":
                if i in [1, 6, 10, 11, 16, 20]:  # 'a' indices for 'Human-Nature'
                    profession_groups_count['Human-Nature'] += 1
                elif i in [4, 9, 14, 19]:  # 'a' indices for 'Human-Technique'
                    profession_groups_count['Human-Technique'] += 1
                elif i in [2, 8, 12, 18]:  # 'a' indices for 'Human-Human'
                    profession_groups_count['Human-Human'] += 1
                elif i in [5, 15]:  # 'a' indices for 'Human-Sign Systems'
                    profession_groups_count['Human-Sign Systems'] += 1
                elif i in [3, 7, 13, 17]:  # 'a' indices for 'Human-Artistic Image'
                    profession_groups_count['Human-Artistic Image'] += 1
            elif value == "b":
                if i in [3, 13]:  # 'b' indices for 'Human-Nature'
                    profession_groups_count['Human-Nature'] += 1
                elif i in [1, 7, 11, 17]:  # 'b' indices for 'Human-Technique'
                    profession_groups_count['Human-Technique'] += 1
                elif i in [4, 6, 14, 16]:  # 'b' indices for 'Human-Human'
                    profession_groups_count['Human-Human'] += 1
                elif i in [2, 9, 10, 12, 19, 20]:  # 'b' indices for 'Human-Sign Systems'
                    profession_groups_count['Human-Sign Systems'] += 1
                elif i in [5, 8, 15, 18]:  # 'b' indices for 'Human-Artistic Image'
                    profession_groups_count['Human-Artistic Image'] += 1


        max_category = max(profession_groups_count, key=profession_groups_count.get)
        max_count = profession_groups_count[max_category]

        answer = "Предлагаемая вами профессиональная группа - это:"
        result = max_category
        result2 = ""
        if language == "KZ":
            submit = "Бастау"
            answer = "Сіздің ұсынылған мамандық тобыңыз"
            if result == 'Human-Nature':
                result = "Мұнда адам жансыз және тірі табиғаттың әртүрлі құбылыстарымен айналысатын профессорлар кіреді, мысалы, биолог, географ, геолог, математик, физик, химик және жаратылыстану ғылымдары санатына жататын басқа мамандықтар.",
                result2 = "Адам Табиғаты"
            elif result == 'Human-Technique':
                result2 = "Адам Техникасы"
                result = "Бұл топқа адам техникамен, оны қолданумен немесе дизайнмен айналысатын әр түрлі жұмыс түрлері кіреді, мысалы, инженер, оператор, машинист, механизатор, дәнекерлеуші және т. б. профессор."
            elif result == 'Human-Human':
                result2 = "Адам-Адам"
                result = "Мұнда адамдардың өзара әрекеттесуін көздейтін мамандықтың барлық түрлері ұсынылған, мысалы, саясат, дін, педагогика, психология, медицина, сауда, құқық."
            elif result == 'Human-Sign Systems':
                result2 = "Адам Белгілері Жүйелері:"
                result = "Бұл топқа құру, оқыту және пайдалануға қатысты мамандықтар кіредіәр түрлі белгілі жүйелер, лингвистика түрлері, математикалық бағдарламалау тілдері, зерттеу нәтижелерін графикалық бейнелеу мүмкіндіктері және т. б."
            elif result == 'Human-Artistic Image':
                result2 = "Адам-Көркем Образ"
                result = "Бұл топ-көркем және шығармашылық жұмыстың әртүрлі түрлері, әдебиет, музыка, театр, бейнелеу өнері."

        elif language == "RU":
            submit = "отправить"
            if result == 'Human-Nature':
                result2 ="Человек-природа"
                result = "Здесь входят профессора, в которых человек владеет делом с разными явлениями неживой и живой природы, например биолог, географ, геолог, математик, физик, химик и другие профессии, относящиеся к разряду естественных наук."
            elif result == 'Human-Technique':
                result2 = "Человек-техника"
                result = "В эту группу профессий включены различные виды трудовой деятельности, в которых человек  имеет дело с техникой, её использованием или конструированием, например профессия инженера, оператора, машиниста, механизатора, сварщика и т.п."
            elif result == 'Human-Human':
                result2 = "Человек-человек"
                result = "Сюда включены все виды профессий, предполагающих взаимодействие людей, например политика, религия, педагогика, психология, медицина, торговля, право "
            elif result == 'Human-Sign Systems':
                result2 = "Человек-знаковые"
                result = "В эту группу включены профессии, касающиеся создания, обучения и использования различных известных систем, видов лингвистики, языков математического программирования, возможностей графического представления результатов изучения и т. п."
            elif result == 'Human-Artistic Image':
                result2 = "Человек-художественный образ:",
                result = "Эта группа представляет собой различные виды художественно-творческого труда, тип литературы, музыки, театра, образное искусство."

        TestResult.objects.create(user_data_id=user_data_id, test_name="Тест-опросник на профориентацию", result=result)

        new_result = TestResult.objects.create(user_data_id=user_data_id, test_name="Тест-опросник на профориентацию", result=result)
        result_id = new_result.id

        # Generate the admin change path
        domain = 'https://gasyrfoundation.com'
        admin_change_path = reverse('admin:test_app_testresult_change', args=(result_id,))
        message_text = "Привет, вот ссылка на результат / Сәлем, нәтижеге сілтеме:"

        # Use the helper function to create the WhatsApp link
        whatsapp_link = create_whatsapp_link(domain, admin_change_path, message_text)

        # Select the appropriate template based on the user's language preference
        user_data = get_object_or_404(UserData, id=user_data_id)
        return render(request, "test_app/first_test/results.html", {
            'result': result,
            'result2': result2,
            'answer': answer,
            'user_data_id': user_data_id,
            'submit_text': submit_text,
            'whatsapp_link': whatsapp_link,  # Include the WhatsApp link
        })
    else:
        # For GET requests, display the test questions filtered by language
        if(language == "KZ"):
            questions = Question_kk.objects.all()
        else:
            questions = Question.objects.all()
        return render(request, 'test_app/first_test/test.html', {
            'questions': questions,
            'user_data_id': user_data_id,
            'submit_text': submit_text
        })


def calculate_holland_type(responses):
    type_counts = {'Р': 0, 'И': 0, 'С': 0, 'К': 0, 'П': 0, 'А': 0}

    answer_key = {
        '1а': 'Р', '2а': 'Р', '3а': 'Р', '4а': 'Р', '5а': 'Р', '16а': 'Р', '17а': 'Р', '18а': 'Р', '19а': 'Р',
        '21а': 'Р', '31а': 'Р', '32а': 'Р', '33а': 'Р', '34а': 'Р',
        '1б': 'И', '6а': 'И', '7а': 'И', '8а': 'И', '9а': 'И', '16б': 'И', '20а': 'И', '22а': 'И', '23а': 'И',
        '24а': 'И', '31б': 'И', '35а': 'И', '36а': 'И', '37а': 'И',
        '2б': 'С', '6б': 'С', '10а': 'С', '11а': 'С', '12а': 'С', '17б': 'С', '29б': 'С', '25а': 'С', '26а': 'С',
        '27а': 'С', '36б': 'С', '38а': 'С', '39а': 'С', '41б': 'С',
        '3б': 'К', '7б': 'К', '10б': 'К', '13а': 'К', '14а': 'К', '18б': 'К', '22б': 'К', '25б': 'К', '28а': 'К',
        '29а': 'К', '32б': 'К', '38б': 'К', '40а': 'К', '42а': 'К',
        '4б': 'П', '8б': 'П', '11б': 'П', '13б': 'П', '15а': 'П', '23б': 'П', '28б': 'П', '30а': 'П', '33б': 'П',
        '35б': 'П', '37б': 'П', '39б': 'П', '40б': 'П',
        '5б': 'А', '9б': 'А', '12б': 'А', '14б': 'А', '15б': 'А', '19б': 'А', '21б': 'А', '24б': 'А', '27б': 'А',
        '29б': 'А', '30б': 'А', '34б': 'А', '41а': 'А', '42б': 'А'
    }

    question_id_to_key_mapping = {
        '169': '1', '170': '2', '171': '3', '172': '4а', '173': '5',
        '174': '16', '175': '17', '176': '18', '177': '19', '178': '21',
        '179': '31', '180': '32', '181': '33', '182': '34',
        '183': '1', '184': '6', '185': '7', '186': '8', '187': '9',
        '188': '16', '189': '20', '190': '22', '191': '23', '192': '24',
        '193': '31', '194': '35', '195': '36', '196': '37',
        '197': '2', '198': '6', '199': '10', '200': '11',
        '201': '12', '202': '17', '203': '29', '204': '25',
        '205': '26', '206': '27', '207': '36', '208': '38',
        '209': '39', '210': '41',
    }

    for question_id, answer in responses.items():
        question_base = question_id_to_key_mapping.get(str(question_id), '')
        question_key = f"{question_base}а" if answer == 'a' else f"{question_base}б"

        if question_key in answer_key:
            type_key = answer_key[question_key]
            type_counts[type_key] += 1

    dominant_type = max(type_counts, key=type_counts.get)
    return dominant_type, type_counts


def holland_test_view(request, user_data_id):
    user_data = get_object_or_404(UserData, id=user_data_id)
    language = user_data.language

    if request.method == "POST":
        responses = {key.replace("response_", ""): value for key, value in request.POST.items() if
                     key.startswith("response_")}
        dominant_type, type_counts = calculate_holland_type(responses)

        # Personality descriptions based on the dominant type
        personality_descriptions = {
            'Р': 'Активность, агрессивность, деловитость, настойчивость, рациональность, практическое мышление, развитые двигательные навыки, пространственное воображение, технические способности',
            'И': 'Аналитический ум, независимость и оригинальность суждений, гармоничное развитие языковых и математических способностей, критичность, любознательность, склонность к фантазии, интенсивная внутренняя жизнь, низкая физическая активность',
            'С': 'Умение общаться, гуманность, способность к сопереживанию, активность, зависимость от окружающих и общественного мнения, приспособление, решение проблем с опорой на эмоции и чувства, преобладание языковых способностей',
            'К': 'Способности к переработке числовой информации, стереотипный подход к проблемам, консервативный характер, подчиняемость, зависимость, следование обычаям, конформность, исполнительность, преобладание математических способностей',
            'П': 'Энергия, импульсивность, энтузиазм, предприимчивость, агрессивность, готовность к риску, оптимизм, уверенность в себе, преобладание языковых способностей, развитые организаторские способности',
            'А': 'Воображение и интуиция, эмоционально сложный взгляд на жизнь, независимость, гибкость и оригинальность мышления, развитые двигательные способности и восприятие'
        }

        personality_description = personality_descriptions.get(dominant_type, 'Description not found.')

        combined_result = f"{dominant_type} - {personality_description}"

        new_result = TestResult.objects.create(user_data_id=user_data_id, test_name="Тест-опросник на определение типа личности",
                                               result=combined_result)
        result_id = new_result.id

        domain = 'https://gasyrfoundation.com'
        admin_path = reverse('admin:test_app_testresult_change', args=(result_id,))
        admin_url = f"{domain}{admin_path}"

        whatsapp_message = f"Привет, вот ссылка на результат / Сәлем, нәтижеге сілтеме: {admin_url}"
        encoded_whatsapp_message = quote(whatsapp_message)
        whatsapp_link = f"https://wa.me/77000660868?text={encoded_whatsapp_message}"

        personality_description = personality_descriptions.get(dominant_type, 'Description not found.')

        return render(request, 'test_app/second_test/holland_results.html', {
            'result': dominant_type,
            'type_counts': type_counts,
            'personality_description': personality_description,
            'text2': 'Ваш Доминантный код Холланда - ',
            'user_data_id': user_data_id,
            'whatsapp_link': whatsapp_link,  # Add this line
            'submit_text': "Return home",
        })

    submit_text = "ПОЛУЧИТЬ РЕЗУЛЬТАТ" if user_data.language != "KZ" else "Бастау"
    if (language == "KZ"):
        questions = HollandQuestion_kk.objects.all()
    else:
        questions = HollandQuestion.objects.all()

    return render(request, 'test_app/second_test/holland_test.html', {
        'questions': questions,
        'user_data_id': user_data_id,
        'submit_text': submit_text,
    })

def preference_test_view(request, user_data_id):
    user_data = get_object_or_404(UserData, id=user_data_id)
    language = user_data.language
    submit_text = "Бастау" if language == "KZ" else "ПОЛУЧИТЬ РЕЗУЛЬТАТ"

    if request.method == 'POST':
        scores = {
            'Work with people': 0,
            'Intellectual work': 0,
            'Technical interests': 0,
            'Aesthetics and art': 0,
            'Physical work': 0,
            'Material interests': 0,
        }

        question_category_map = {
            '2a': 'Work with people', '4a': 'Work with people', '6b': 'Work with people', '9a': 'Work with people',
            '12b': 'Work with people',
            '16a': 'Work with people', '17b': 'Work with people', '19b': 'Work with people', '23b': 'Work with people',
            '28b': 'Work with people',
            '4b': 'Intellectual work', '7a': 'Intellectual work', '10b': 'Intellectual work',
            '13a': 'Intellectual work', '14b': 'Intellectual work',
            '18a': 'Intellectual work', '20a': 'Intellectual work', '21b': 'Intellectual work',
            '26b': 'Intellectual work', '30a': 'Intellectual work',
            '1b': 'Technical interests', '3b': 'Technical interests', '6a': 'Technical interests',
            '8b': 'Technical interests', '12a': 'Technical interests',
            '14a': 'Technical interests', '15b': 'Technical interests', '25a': 'Technical interests',
            '26a': 'Technical interests', '29b': 'Technical interests',
            '1a': 'Aesthetics and art', '5b': 'Aesthetics and art', '8a': 'Aesthetics and art',
            '10a': 'Aesthetics and art', '11b': 'Aesthetics and art',
            '17a': 'Aesthetics and art', '21a': 'Aesthetics and art', '23a': 'Aesthetics and art',
            '24b': 'Aesthetics and art', '28a': 'Aesthetics and art',
            '2b': 'Physical work', '5a': 'Physical work', '13b': 'Physical work', '15a': 'Physical work',
            '18b': 'Physical work',
            '20b': 'Physical work', '22a': 'Physical work', '24a': 'Physical work', '25b': 'Physical work',
            '27a': 'Physical work',
            '3a': 'Material interests', '7b': 'Material interests', '9b': 'Material interests',
            '11a': 'Material interests', '16b': 'Material interests',
            '19a': 'Material interests', '22b': 'Material interests', '27b': 'Material interests',
            '29a': 'Material interests', '30b': 'Material interests',
        }

        for key, value in request.POST.items():
            if key.startswith('question'):
                question_id, option = key.split('_')[1], value[-2]
                if option == '2':
                    option = 'b'
                else:
                    option = 'a'
                score = int(value[:-1])
                category = question_category_map.get(f'{question_id}{option}')
                if category:
                    scores[category] += score

        # Determine the preferred category
        preferred_category = max(scores, key=scores.get)

        if language == "KZ":
            text = "Сіздің қалаған санатыңыз:"
            if preferred_category == "Work with people":
                preferred_category = "Адамдармен жұмыс: мұғалім, мұғалім, гид, тәрбиеші, әлеуметтанушы, психолог, персонал менеджері, тергеуші."

            elif preferred_category == "Intellectual work":
                preferred_category = "Интеллектуалды жұмыс: зерттеуші ғалым (математик, физик, химик, кибернетик, археолог, геолог), инженер, заңгер, дәрігер, эколог, сәулетші, продюсер."

            elif preferred_category == "Technical interests":
                preferred_category = "Техникалық қызығушылықтар: программист, электротехник, радиотехник, Web -мастер, статистик, водитель, технолог, диспетчер, секретарь-машинистка, телефонист."

            elif preferred_category == "Aesthetics and art":
                preferred_category = "Эстетика және өнер: суретші, дизайнер, жазушы, ақын, режиссер, суретші, дизайнер, косметолог, костюмер, макияж суретшісі, кондитер, тігінші-кутюрье, гүл өсіруші."

            elif preferred_category == "Physical work":
                preferred_category = "Физикалық жұмыс: фотограф, экспедитор, шаштараз, бармен, даяшы, стюардесса, сатушы, кескіш, жөндеуші, кассир, мейірбике, бригадир, қоймашы, пошташы, фермер, жүк көлігі жүргізушісі, полиция қызметкері, әскери."

            elif preferred_category == "Material interests":
                preferred_category = "Материалдық мүдделер: жоспарлы-экономикалық жұмыс түрлері: экономист, әкімші, менеджер, кәсіпкер, аудитор, жарнама жөніндегі маман, брокер, сақтандыру компанияларының агенті, коммерсант, импорттаушы."

        elif language == "RU":
            text = "Ваша предпочтительная категория - это:"

            if preferred_category == "Work with people":
                preferred_category = "Работа с людьми: учитель, педагог, экскурсовод, воспитатель,  социолог, психолог, менеджер по персоналу, следователь."

            elif preferred_category == "Intellectual work":
                preferred_category = "Интеллектуальная работа: ученый-исследователь (математик, физик, химик, кибернетик, археолог, геолог),  инженер, юрист, врач, эколог, архитектор, продюсер."

            elif preferred_category == "Technical interests":
                preferred_category = "Технические интересы: программист, электротехник, радиотехник, Web -мастер, статистик, водитель, технолог, диспетчер, секретарь-машинистка, телефонист."

            elif preferred_category == "Aesthetics and art":
                preferred_category = "Эстетика и искусство: художник, дизайнер, писатель, поэт,  режиссер, артист, конструктор, косметолог, костюмер, гример, кондитер, портной-кутюрье, цветовод."

            elif preferred_category == "Physical work":
                preferred_category = "Физический труд: спортсмен, фотограф, экспедитор, парикмахер,  бармен, официант, стюардесса, продавец, закройщик, специалист по ремонту, кассир, медперсонал, бригадир, кладовщик,  почтальон,  фермер,  водитель-дальнобойщик, полицейский, военный."

            elif preferred_category == "Material interests":
                preferred_category = "Материальные интересы: планово-экономических видов работ: экономист, администратор, менеджер, предприниматель, аудитор, специалист по рекламе, брокер, агент страховых компаний, коммерсант, завхоз."

        TestResult.objects.create(user_data_id=user_data_id, test_name="Тест на профессиональные предпочтения", result=preferred_category)

        new_result = TestResult.objects.create(
            user_data=user_data,
            test_name="Тест на профессиональные предпочтения",
            result=preferred_category
        )

        # Get the absolute admin URL for the new TestResult instance
        domain = 'https://gasyrfoundation.com'
        admin_change_path = reverse('admin:test_app_testresult_change', args=(new_result.id,))
        admin_url = f"{domain}{admin_change_path}"

        # Construct the WhatsApp URL
        whatsapp_message = f"Привет, вот ссылка на результат / Сәлем, нәтижеге сілтеме: {admin_url}"
        encoded_whatsapp_message = quote(whatsapp_message)
        whatsapp_link = f"https://wa.me/77000660868?text={encoded_whatsapp_message}"

        # Render the template with the new context
        return render(request, 'test_app/third_test/preference_result.html', {
            'preferred_category': preferred_category,
            'text': text,
            'user_data_id': user_data_id,
            'submit_text': submit_text,
            'whatsapp_link': whatsapp_link  # Pass the WhatsApp link to the template
        })
    else:
        if(language == "KZ"):

            questions = PreferenceQuestion_kk.objects.all()
        else:
            questions = PreferenceQuestion.objects.all()
        return render(request, 'test_app/third_test/preference_test.html', {'questions': questions,
                                                                            'user_data_id': user_data_id,
                                                                            'submit_text': submit_text
                                                                            })
# def survey_view(request, user_data_id):
#     user_data = get_object_or_404(UserData, id=user_data_id)
#     user_language = user_data.language
#     submit_text = "Бастау" if user_language == "KZ" else "ПОЛУЧИТЬ РЕЗУЛЬТАТ"
#
#
#     if request.method == 'POST':
#         if(user_language == "KZ"):
#             form = SurveyForm_kk(request.POST)
#         else:
#             form = SurveyForm(request.POST)
#         if form.is_valid():
#             answers = form.cleaned_data
#             results = answers.values()
#
#             # Инициализация списка результатов для каждой категории
#             results_by_category = [0] * 29
#             levels_mapping_ru = {
#                 -12: "высшая степень отрицания данного интереса",
#                 -11: "высшая степень отрицания данного интереса",
#                 -10: "высшая степень отрицания данного интереса",
#                 -9: "высшая степень отрицания данного интереса",
#                 -8: "высшая степень отрицания данного интереса",
#                 -7: "выраженный интерес",
#                 -6: "выраженный интерес",
#                 -5: "выраженный интерес",
#                 -4: "интерес выражен слабо",
#                 -3: "интерес выражен слабо",
#                 -2: "интерес выражен слабо",
#                 -1: "интерес выражен слабо",
#                 0: "интерес отрицается",
#                 1: "интерес выражен слабо",
#                 2: "интерес выражен слабо",
#                 3: "интерес выражен слабо",
#                 4: "интерес выражен слабо",
#                 5: "выраженный интерес",
#                 6: "выраженный интерес",
#                 7: "выраженный интерес",
#                 8: "ярко выраженный интерес",
#                 9: "ярко выраженный интерес",
#                 10: "ярко выраженный интерес",
#                 11: "ярко выраженный интерес",
#                 12: "ярко выраженный интерес",
#             }
#
#             levels_mapping_kk = {
#                 -12: "осы қызығушылықтың ең жоғары дәрежесінің теріске шығарылуы",
#                 -11: "осы қызығушылықтың ең жоғары дәрежесінің теріске шығарылуы",
#                 -10: "осы қызығушылықтың ең жоғары дәрежесінің теріске шығарылуы",
#                 -9: "осы қызығушылықтың ең жоғары дәрежесінің теріске шығарылуы",
#                 -8: "осы қызығушылықтың ең жоғары дәрежесінің теріске шығарылуы",
#                 -7: "білдірілген қызығушылық",
#                 -6: "білдірілген қызығушылық",
#                 -5: "білдірілген қызығушылық",
#                 -4: "қызығушылық аз білдірілген",
#                 -3: "қызығушылық аз білдірілген",
#                 -2: "қызығушылық аз білдірілген",
#                 -1: "қызығушылық аз білдірілген",
#                 0: "қызығушылық теріске шығарылады",
#                 1: "қызығушылық аз білдірілген",
#                 2: "қызығушылық аз білдірілген",
#                 3: "қызығушылық аз білдірілген",
#                 4: "қызығушылық аз білдірілген",
#                 5: "білдірілген қызығушылық",
#                 6: "білдірілген қызығушылық",
#                 7: "білдірілген қызығушылық",
#                 8: "қатты білдірілген қызығушылық",
#                 9: "қатты білдірілген қызығушылық",
#                 10: "қатты білдірілген қызығушылық",
#                 11: "қатты білдірілген қызығушылық",
#                 12: "қатты білдірілген қызығушылық",
#             }
#             if(user_language == "KZ"):
#                 levels_mapping = levels_mapping_kk
#             else:
#                 levels_mapping = levels_mapping_ru
#
#             # Определение значений для каждой переменной в зависимости от ответов
#             for i, result in enumerate(results, start=1):
#                 question_index = (i - 1) % 29  # Вычисляем индекс вопроса от 0 до 28 для каждого i
#                 if result == '++':
#                     results_by_category[question_index] += 2
#                 elif result == '+':
#                     results_by_category[question_index] += 1
#                 elif result == '-':
#                     results_by_category[question_index] -= 1
#                 elif result == '--':
#                     results_by_category[question_index] -= 2
#                 else:
#                     pass  # Ничего не делаем, если ответ не указан
#
#             categories_ru = {
#                 "Биология": levels_mapping.get(results_by_category[0], "Недопустимое значение"),
#                 "География": levels_mapping.get(results_by_category[1], "Недопустимое значение"),
#                 "Геология": levels_mapping.get(results_by_category[2], "Недопустимое значение"),
#                 "Медицина": levels_mapping.get(results_by_category[3], "Недопустимое значение"),
#                 "Легкая и пищевая промышленность": levels_mapping.get(results_by_category[4], "Недопустимое значение"),
#                 "Физика": levels_mapping.get(results_by_category[5], "Недопустимое значение"),
#                 "Химия": levels_mapping.get(results_by_category[6], "Недопустимое значение"),
#                 "Техника": levels_mapping.get(results_by_category[7], "Недопустимое значение"),
#                 "Электро- и радиотехника": levels_mapping.get(results_by_category[8], "Недопустимое значение"),
#                 "Металлообработка": levels_mapping.get(results_by_category[9], "Недопустимое значение"),
#                 "Деревообработка": levels_mapping.get(results_by_category[10], "Недопустимое значение"),
#                 "Строительство": levels_mapping.get(results_by_category[11], "Недопустимое значение"),
#                 "Транспорт": levels_mapping.get(results_by_category[12], "Недопустимое значение"),
#                 "Авиация, морское дело": levels_mapping.get(results_by_category[13], "Недопустимое значение"),
#                 "Военные специальности": levels_mapping.get(results_by_category[14], "Недопустимое значение"),
#                 "История": levels_mapping.get(results_by_category[15], "Недопустимое значение"),
#                 "Литература": levels_mapping.get(results_by_category[16], "Недопустимое значение"),
#                 "Журналистика": levels_mapping.get(results_by_category[17], "Недопустимое значение"),
#                 "Общественная деятельность": levels_mapping.get(results_by_category[18], "Недопустимое значение"),
#                 "Педагогика": levels_mapping.get(results_by_category[19], "Недопустимое значение"),
#                 "Юриспруденция": levels_mapping.get(results_by_category[20], "Недопустимое значение"),
#                 "Сфера обслуживания": levels_mapping.get(results_by_category[21], "Недопустимое значение"),
#                 "Математика": levels_mapping.get(results_by_category[22], "Недопустимое значение"),
#                 "Экономика": levels_mapping.get(results_by_category[23], "Недопустимое значение"),
#                 "Иностранные языки": levels_mapping.get(results_by_category[24], "Недопустимое значение"),
#                 "Изобразительное искусство": levels_mapping.get(results_by_category[25], "Недопустимое значение"),
#                 "Сценическое искусство": levels_mapping.get(results_by_category[26], "Недопустимое значение"),
#                 "Музыка": levels_mapping.get(results_by_category[27], "Недопустимое значение"),
#                 "Физкультура и спорт": levels_mapping.get(results_by_category[28], "Недопустимое значение")
#             }
#
#             categories_kk = {
#                 "Биология": levels_mapping.get(results_by_category[0], "Жарамсыз мән"),
#                 "География": levels_mapping.get(results_by_category[1], "Жарамсыз мән"),
#                 "Геология": levels_mapping.get(results_by_category[2], "Жарамсыз мән"),
#                 "Медицина": levels_mapping.get(results_by_category[3], "Жарамсыз мән"),
#                 "Легкая и пищевая промышленность": levels_mapping.get(results_by_category[4], "Жарамсыз мән"),
#                 "Физика": levels_mapping.get(results_by_category[5], "Жарамсыз мән"),
#                 "Химия": levels_mapping.get(results_by_category[6], "Жарамсыз мән"),
#                 "Техника": levels_mapping.get(results_by_category[7], "Жарамсыз мән"),
#                 "Электро- и радиотехника": levels_mapping.get(results_by_category[8], "Жарамсыз мән"),
#                 "Металлообработка": levels_mapping.get(results_by_category[9], "Жарамсыз мән"),
#                 "Деревообработка": levels_mapping.get(results_by_category[10], "Жарамсыз мән"),
#                 "Строительство": levels_mapping.get(results_by_category[11], "Жарамсыз мән"),
#                 "Транспорт": levels_mapping.get(results_by_category[12], "Жарамсыз мән"),
#                 "Авиация, морское дело": levels_mapping.get(results_by_category[13], "Жарамсыз мән"),
#                 "Военные специальности": levels_mapping.get(results_by_category[14], "Жарамсыз мән"),
#                 "История": levels_mapping.get(results_by_category[15], "Жарамсыз мән"),
#                 "Литература": levels_mapping.get(results_by_category[16], "Жарамсыз мән"),
#                 "Журналистика": levels_mapping.get(results_by_category[17], "Жарамсыз мән"),
#                 "Общественная деятельность": levels_mapping.get(results_by_category[18], "Жарамсыз мән"),
#                 "Педагогика": levels_mapping.get(results_by_category[19], "Жарамсыз мән"),
#                 "Юриспруденция": levels_mapping.get(results_by_category[20], "Жарамсыз мән"),
#                 "Сфера обслуживания": levels_mapping.get(results_by_category[21], "Жарамсыз мән"),
#                 "Математика": levels_mapping.get(results_by_category[22], "Жарамсыз мән"),
#                 "Экономика": levels_mapping.get(results_by_category[23], "Жарамсыз мән"),
#                 "Иностранные языки": levels_mapping.get(results_by_category[24], "Жарамсыз мән"),
#                 "Изобразительное искусство": levels_mapping.get(results_by_category[25], "Жарамсыз мән"),
#                 "Сценическое искусство": levels_mapping.get(results_by_category[26], "Жарамсыз мән"),
#                 "Музыка": levels_mapping.get(results_by_category[27], "Жарамсыз мән"),
#                 "Физкультура и спорт": levels_mapping.get(results_by_category[28], "Жарамсыз мән")
#             }
#
#
#             if(user_language == "KZ"):
#                 text = "Сауалнама нәтижелері"
#                 categories = categories_kk
#             else:
#                 text = "Результаты опроса"
#                 categories = categories_ru
#
#             results = {'++': 0, '+': 0, '0': 0, '-': 0, '--': 0}
#
#             for answer in answers.values():
#                 results[answer] += 1
#             # Здесь можно сделать что-то с results, например, передать их в шаблон
#             TestResult.objects.create(user_data_id=user_data_id, test_name="Survey", result=str(categories))
#
#             new_result = TestResult.objects.create(user_data_id=user_data_id, test_name="Survey",
#                                                    result=str(categories))
#             result_id = new_result.id
#
#             # Generate the admin change path
#             domain = 'https://gasyrfoundation.com'
#             admin_change_path = reverse('admin:test_app_testresult_change', args=(result_id,))
#             message_text = "Привет, вот ссылка на результат / Сәлем, нәтижеге сілтеме:"
#
#             # Use the helper function to create the WhatsApp link
#             whatsapp_link = create_whatsapp_link(domain, admin_change_path, message_text)
#
#             return render(request, "test_app/fourth_test/survey_result.html", {
#                 'categories': categories,
#                 'text': text,
#                 'whatsapp_link': whatsapp_link,
#                 'user_data_id': user_data_id,
#                 'submit_text': submit_text
#             })
#     else:
#         if (user_language == "KZ"):
#             form = SurveyForm_kk(request.POST)
#         else:
#             form = SurveyForm(request.POST)
#         return render(request, "test_app/fourth_test/survey_test.html", {'form': form,
#                                                                          'user_data_id': user_data_id,
#                                                                          'submit_text': submit_text})


from django.shortcuts import render
from .forms import CareerAnchorForm
from .models import CareerAnchorQuestion


def career_anchor_test_view(request, user_data_id):
    user_data = get_object_or_404(UserData, id=user_data_id)
    language = user_data.language
    submit_text = "Бастау" if language == "KZ" else "ПОЛУЧИТЬ РЕЗУЛЬТАТ"
    form_class = CareerAnchorForm_kk if language == "KZ" else CareerAnchorForm
    form = form_class(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        career_orientations_scores = {
            'Профессиональная компетентность: Быть профессионалом, мастером в своем деле. Эта ориентация связана с наличием способностей и талантов в определенной области. Люди с такой ориентацией хотят быть мастерами своего дела, они бывают особенно счастливы, когда достигают успеха в профессиональной сфере, но быстро теряют интерес к работе, которая не позволяет развивать их способности. Вряд ли их заинтересует даже значительно более высокая должность, если она не связана с их профессиональными компетенциями. Они ищут признания своих талантов, что должно выражаться в статусе, соответствующем их мастерству. Они готовы управлять другими в пределах своей компетенции, но управление не представляет для них особого интереса. Поэтому многие из этой категории отвергают работу руководителя, управление рассматривают как необходимое условие для продвижения в своей профессиональной сфере.': 0,
            'Менеджмент: Управлять – людьми, проектами, бизнес-процессами и т.п. Для этих людей первостепенное значение имеет ориентация личности на интеграцию усилий других людей, полнота ответственности за конечный результат и соединение различных функций организации. С возрастом и опытом эта карьерная ориентация проявляется сильнее. Возможности для лидерства, высокого дохода, повышенных уровней ответственности и вклад в успех своей организации являются ключевыми ценностями и мотивами. Самое главное для них – управление: людьми, проектами, любыми бизнес-процессами – это в целом не имеет принципиального значения. Центральное понятие их профессионального развития – власть, осознание того, что от них зависит принятие ключевых решений. Причем для них не является принципиальным управление собственным проектом или целым бизнесом, скорее наоборот, они в большей степени ориентированы на построение карьеры в наемном менеджменте, но при условии, что им будут делегированы значительные полномочия. Человек с такой ориентацией будет считать, что не достиг цели своей карьеры, пока не займет должность, на которой будет управлять различными сторонами деятельности предприятия.': 0,
            'Автономия (независимость): Главное в работе – это свобода и независимость. Первичная забота личности с такой ориентацией – освобождение от организационных правил, предписаний и ограничений. Они испытывают трудности, связанные с установленными правилами, процедурами, рабочим днем, дисциплиной, формой одежды и т.д. Они любят выполнять работу своим способом, темпом и по собственным стандартам. Они не любят, когда работа вмешивается в их частную жизнь, поэтому предпочитают делать независимую карьеру собственным путем. Они скорее выберут низкосортную работу, чем откажутся от автономии и независимости. Для них первоочередная задача развития карьеры – получить возможность работать самостоятельно, самому решать, как, когда и что делать для достижения тех или иных целей. Карьера для них – это, прежде всего, способ реализации их свободы, поэтому любые рамки и строгое подчинение оттолкнут их даже от внешне привлекательной вакансии. Такой человек может работать в организации, которая обеспечивает достаточную степень свободы.': 0,
            'Стабильность работы: Стабильная, надежная работа на длительное времяЭти люди испытывают потребность в безопасности, защите и возможности прогнозирования и будут искать постоянную работу с минимальной вероятностью увольнения. Эти люди отождествляют свою работу со своей карьерой. Их потребность в безопасности и стабильности ограничивает выбор вариантов карьеры. Авантюрные или краткосрочные проекты и только становящиеся на ноги компании их, скорее всего, не привлекают. Они очень ценят социальные гарантии, которые может предложить работодатель, и, как правило, их выбор места работы связан именно с длительным контрактом и стабильным положением компании на рынке. Такие люди ответственность за управление своей карьерой перекладывают на нанимателя.': 0,
            'Стабильность места жительства: Главное – жить в своем городе (минимум переездов, командировок). Важнее остаться на одном месте жительства, чем получить повышение или новую работу на новой местности. Переезд для таких людей неприемлем, и даже частые командировки являются для них негативным фактором при рассмотрении предложения о работе.': 0,
            'Служение Воплощать в работе свои идеалы и ценности. Данная ценностная ориентация характерна для людей, занимающихся делом по причине желания реализовать в своей работе главные ценности. Они часто ориентированы больше на ценности, чем на требующиеся в данном виде работы способности. Они стремятся приносить пользу людям, обществу, для них очень важно видеть конкретные плоды своей работы, даже если они и не выражены в материальном эквиваленте. Основной тезис построения их карьеры – получить возможность максимально эффективно использовать их таланты и опыт для реализации общественно важной цели. Люди, ориентированные на служение, общительны и часто консервативны. Человек с такой ориентацией не будет работать в организации, которая враждебна его целям и ценностям.': 0,
            'Вызов: Сделать невозможное – возможным, решать уникальные задачи. Эти люди считают успехом преодоление непреодолимых препятствий, решение неразрешимых проблем или просто выигрыш. Они ориентированы на то, чтобы “бросать вызов”. Для одних людей вызов представляет более трудная работа, для других это — конкуренция и межличностные отношения. Они ориентированы на решение заведомо сложных задач, преодоление препятствий ради победы в конкурентной борьбе. Они чувствуют себя преуспевающими только тогда, когда постоянно вовлечены в решение трудных проблем или в ситуацию соревнования. Карьера для них – это постоянный вызов их профессионализму, и они всегда готовы его принять. Социальная ситуация чаще всего рассматривается с позиции “выигрыша – проигрыша”. Процесс борьбы и победа более важна для них, чем конкретная область деятельности или квалификация. Новизна,разнообразие и вызов имеют для них очень большую ценность, и, если все идет слишком просто, им становиться скучно.': 0,
            'Интеграция стилей жизни: Сохранение гармонии между сложившейся личной жизнью и карьерой. Для людей этой категории карьера должна ассоциироваться с общим стилем жизни, уравновешивая потребности человека, семьи и карьеры. Они хотят, чтобы организационные отношения отражали бы уважение к их личным и семейным проблемам. Выбирать и поддерживать определенный образ жизни для них важнее, чем добиваться успеха в карьере. Развитие карьеры их привлекает только в том случае, если она не нарушает привычный им стиль жизни и окружение. Для них важно, чтобы все было уравновешено – карьера, семья, личные интересы и т.п. Жертвовать чем-то одним ради другого им явно не свойственно. Такие люди обычно в своем поведении проявляют конформность (тенденция изменять свое поведение в зависимости от влияния других людей, с тем, чтобы оно соответствовало мнению окружающих)': 0,
            'Предпринимательство Создавать новые организации, товары, услуги. Этим людям нравится создавать новые организации, товары или услуги, которые могут быть отождествлены с их усилиями. Работать на других – это не их, они – предприниматели по духу, и цель их карьеры – создать что-то новое, организовать свое дело, воплотить в жизнь идею, всецело принадлежащую только им. Вершина карьеры в их понимании – собственный бизнес.': 0,
        }
        question_orientations_mapping = {
            'Профессиональная компетентность: Быть профессионалом, мастером в своем деле. Эта ориентация связана с наличием способностей и талантов в определенной области. Люди с такой ориентацией хотят быть мастерами своего дела, они бывают особенно счастливы, когда достигают успеха в профессиональной сфере, но быстро теряют интерес к работе, которая не позволяет развивать их способности. Вряд ли их заинтересует даже значительно более высокая должность, если она не связана с их профессиональными компетенциями. Они ищут признания своих талантов, что должно выражаться в статусе, соответствующем их мастерству. Они готовы управлять другими в пределах своей компетенции, но управление не представляет для них особого интереса. Поэтому многие из этой категории отвергают работу руководителя, управление рассматривают как необходимое условие для продвижения в своей профессиональной сфере.': [
                83, 91, 99, 107, 115],
            'Менеджмент: Управлять – людьми, проектами, бизнес-процессами и т.п. Для этих людей первостепенное значение имеет ориентация личности на интеграцию усилий других людей, полнота ответственности за конечный результат и соединение различных функций организации. С возрастом и опытом эта карьерная ориентация проявляется сильнее. Возможности для лидерства, высокого дохода, повышенных уровней ответственности и вклад в успех своей организации являются ключевыми ценностями и мотивами. Самое главное для них – управление: людьми, проектами, любыми бизнес-процессами – это в целом не имеет принципиального значения. Центральное понятие их профессионального развития – власть, осознание того, что от них зависит принятие ключевых решений. Причем для них не является принципиальным управление собственным проектом или целым бизнесом, скорее наоборот, они в большей степени ориентированы на построение карьеры в наемном менеджменте, но при условии, что им будут делегированы значительные полномочия. Человек с такой ориентацией будет считать, что не достиг цели своей карьеры, пока не займет должность, на которой будет управлять различными сторонами деятельности предприятия.': [
                84, 92, 100, 108, 116],
            'Автономия (независимость): Главное в работе – это свобода и независимость. Первичная забота личности с такой ориентацией – освобождение от организационных правил, предписаний и ограничений. Они испытывают трудности, связанные с установленными правилами, процедурами, рабочим днем, дисциплиной, формой одежды и т.д. Они любят выполнять работу своим способом, темпом и по собственным стандартам. Они не любят, когда работа вмешивается в их частную жизнь, поэтому предпочитают делать независимую карьеру собственным путем. Они скорее выберут низкосортную работу, чем откажутся от автономии и независимости. Для них первоочередная задача развития карьеры – получить возможность работать самостоятельно, самому решать, как, когда и что делать для достижения тех или иных целей. Карьера для них – это, прежде всего, способ реализации их свободы, поэтому любые рамки и строгое подчинение оттолкнут их даже от внешне привлекательной вакансии. Такой человек может работать в организации, которая обеспечивает достаточную степень свободы.': [
                85, 93, 101, 109, 117],
            'Стабильность работы: Стабильная, надежная работа на длительное времяЭти люди испытывают потребность в безопасности, защите и возможности прогнозирования и будут искать постоянную работу с минимальной вероятностью увольнения. Эти люди отождествляют свою работу со своей карьерой. Их потребность в безопасности и стабильности ограничивает выбор вариантов карьеры. Авантюрные или краткосрочные проекты и только становящиеся на ноги компании их, скорее всего, не привлекают. Они очень ценят социальные гарантии, которые может предложить работодатель, и, как правило, их выбор места работы связан именно с длительным контрактом и стабильным положением компании на рынке. Такие люди ответственность за управление своей карьерой перекладывают на нанимателя.': [
                86, 94, 102, 110],
            'Стабильность места жительства: Главное – жить в своем городе (минимум переездов, командировок). Важнее остаться на одном месте жительства, чем получить повышение или новую работу на новой местности. Переезд для таких людей неприемлем, и даже частые командировки являются для них негативным фактором при рассмотрении предложения о работе.': [
                87, 95, 103],
            'Служение Воплощать в работе свои идеалы и ценности. Данная ценностная ориентация характерна для людей, занимающихся делом по причине желания реализовать в своей работе главные ценности. Они часто ориентированы больше на ценности, чем на требующиеся в данном виде работы способности. Они стремятся приносить пользу людям, обществу, для них очень важно видеть конкретные плоды своей работы, даже если они и не выражены в материальном эквиваленте. Основной тезис построения их карьеры – получить возможность максимально эффективно использовать их таланты и опыт для реализации общественно важной цели. Люди, ориентированные на служение, общительны и часто консервативны. Человек с такой ориентацией не будет работать в организации, которая враждебна его целям и ценностям.': [
                88, 96, 104, 112, 120],
            'Вызов: Сделать невозможное – возможным, решать уникальные задачи. Эти люди считают успехом преодоление непреодолимых препятствий, решение неразрешимых проблем или просто выигрыш. Они ориентированы на то, чтобы “бросать вызов”. Для одних людей вызов представляет более трудная работа, для других это — конкуренция и межличностные отношения. Они ориентированы на решение заведомо сложных задач, преодоление препятствий ради победы в конкурентной борьбе. Они чувствуют себя преуспевающими только тогда, когда постоянно вовлечены в решение трудных проблем или в ситуацию соревнования. Карьера для них – это постоянный вызов их профессионализму, и они всегда готовы его принять. Социальная ситуация чаще всего рассматривается с позиции “выигрыша – проигрыша”. Процесс борьбы и победа более важна для них, чем конкретная область деятельности или квалификация. Новизна,разнообразие и вызов имеют для них очень большую ценность, и, если все идет слишком просто, им становиться скучно.': [
                89, 97, 105, 113, 121],
            'Интеграция стилей жизни: Сохранение гармонии между сложившейся личной жизнью и карьерой. Для людей этой категории карьера должна ассоциироваться с общим стилем жизни, уравновешивая потребности человека, семьи и карьеры. Они хотят, чтобы организационные отношения отражали бы уважение к их личным и семейным проблемам. Выбирать и поддерживать определенный образ жизни для них важнее, чем добиваться успеха в карьере. Развитие карьеры их привлекает только в том случае, если она не нарушает привычный им стиль жизни и окружение. Для них важно, чтобы все было уравновешено – карьера, семья, личные интересы и т.п. Жертвовать чем-то одним ради другого им явно не свойственно. Такие люди обычно в своем поведении проявляют конформность (тенденция изменять свое поведение в зависимости от влияния других людей, с тем, чтобы оно соответствовало мнению окружающих)': [
                90, 98, 106, 114, 122],
            'Предпринимательство Создавать новые организации, товары, услуги. Этим людям нравится создавать новые организации, товары или услуги, которые могут быть отождествлены с их усилиями. Работать на других – это не их, они – предприниматели по духу, и цель их карьеры – создать что-то новое, организовать свое дело, воплотить в жизнь идею, всецело принадлежащую только им. Вершина карьеры в их понимании – собственный бизнес.': [
                80, 88, 96, 104, 112],
        }

        for question_id, score in form.cleaned_data.items():
            q_id = int(question_id.split('_')[1])
            score = int(score)
            for orientation, questions in question_orientations_mapping.items():
                if q_id in questions:
                    career_orientations_scores[orientation] += score
                    found = True

        max_orientation = max(career_orientations_scores, key=career_orientations_scores.get)
        max_score = career_orientations_scores[max_orientation]

        # Localize the result text based on language
        if language == "KZ":
            if max_orientation == 'Профессиональная компетентность: Быть профессионалом, мастером в своем деле. Эта ориентация связана с наличием способностей и талантов в определенной области. Люди с такой ориентацией хотят быть мастерами своего дела, они бывают особенно счастливы, когда достигают успеха в профессиональной сфере, но быстро теряют интерес к работе, которая не позволяет развивать их способности. Вряд ли их заинтересует даже значительно более высокая должность, если она не связана с их профессиональными компетенциями. Они ищут признания своих талантов, что должно выражаться в статусе, соответствующем их мастерству. Они готовы управлять другими в пределах своей компетенции, но управление не представляет для них особого интереса. Поэтому многие из этой категории отвергают работу руководителя, управление рассматривают как необходимое условие для продвижения в своей профессиональной сфере.':
                max_orientation = "Кәсіби құзыреттілік"

            elif (
                    max_orientation == 'Менеджмент: Управлять – людьми, проектами, бизнес-процессами и т.п. Для этих людей первостепенное значение имеет ориентация личности на интеграцию усилий других людей, полнота ответственности за конечный результат и соединение различных функций организации. С возрастом и опытом эта карьерная ориентация проявляется сильнее. Возможности для лидерства, высокого дохода, повышенных уровней ответственности и вклад в успех своей организации являются ключевыми ценностями и мотивами. Самое главное для них – управление: людьми, проектами, любыми бизнес-процессами – это в целом не имеет принципиального значения. Центральное понятие их профессионального развития – власть, осознание того, что от них зависит принятие ключевых решений. Причем для них не является принципиальным управление собственным проектом или целым бизнесом, скорее наоборот, они в большей степени ориентированы на построение карьеры в наемном менеджменте, но при условии, что им будут делегированы значительные полномочия. Человек с такой ориентацией будет считать, что не достиг цели своей карьеры, пока не займет должность, на которой будет управлять различными сторонами деятельности предприятия.'):
                max_orientation = "Басқару: Өз ісінің кәсіби маманы, шебері болыңыз. Бұл бағыт белгілі бір салада қабілет пен дарындылықтың болуымен байланысты. Мұндай бағдары бар адамдар өз ісінің шебері болғысы келеді, олар кәсіби салада табысқа жеткенде ерекше қуанады, бірақ қабілеттерін дамытуға мүмкіндік бермейтін жұмысқа деген қызығушылықтары тез жоғалады. Егер бұл олардың кәсіби құзыреттіліктеріне байланысты болмаса, олар тіпті айтарлықтай жоғары лауазымға қызығушылық танытуы екіталай. Олар өз таланттарын тануға ұмтылады, бұл олардың шеберлігіне сәйкес мәртебеде көрсетілуі керек. Олар өз құзыреті шегінде басқаларды басқаруға дайын, бірақ менеджмент олар үшін ерекше қызығушылық тудырмайды. Сондықтан бұл санаттағылардың көпшілігі менеджердің жұмысын жоққа шығарады, менеджмент олардың кәсіби саласында ілгерілеудің қажетті шарты болып саналады."

            elif (
                    max_orientation == 'Автономия (независимость): Главное в работе – это свобода и независимость. Первичная забота личности с такой ориентацией – освобождение от организационных правил, предписаний и ограничений. Они испытывают трудности, связанные с установленными правилами, процедурами, рабочим днем, дисциплиной, формой одежды и т.д. Они любят выполнять работу своим способом, темпом и по собственным стандартам. Они не любят, когда работа вмешивается в их частную жизнь, поэтому предпочитают делать независимую карьеру собственным путем. Они скорее выберут низкосортную работу, чем откажутся от автономии и независимости. Для них первоочередная задача развития карьеры – получить возможность работать самостоятельно, самому решать, как, когда и что делать для достижения тех или иных целей. Карьера для них – это, прежде всего, способ реализации их свободы, поэтому любые рамки и строгое подчинение оттолкнут их даже от внешне привлекательной вакансии. Такой человек может работать в организации, которая обеспечивает достаточную степень свободы.'):
                max_orientation = "Автономия (тәуелсіздік): басқару – адамдар, жобалар, бизнес-процестер және т.б. Бұл адамдар үшін жеке тұлғаның басқа адамдардың күш-жігерін біріктіруге бағдарлануы, түпкілікті нәтиже үшін толық жауапкершілік және ұйымның әртүрлі функцияларын байланыстыру маңызды болып табылады. Жасы мен тәжірибесінің арқасында бұл мансаптық бағыт айқынырақ болады. Көшбасшылық мүмкіндіктері, жоғары табыс, жауапкершілік деңгейінің жоғарылауы және ұйымның табысына үлес қосу - негізгі құндылықтар мен мотивациялар. Олар үшін ең маңыздысы – менеджмент: адамдар, жобалар, кез келген бизнес-процестер – бұл әдетте принципті маңызды емес. Олардың кәсіби дамуының орталық концепциясы – билік, негізгі шешімдердің соларға байланысты екенін түсіну. Оның үстіне, олар үшін жеке жобаны немесе тұтас бизнесті басқару маңызды емес, керісінше, олар жалдамалы басқаруда мансап құруға көбірек көңіл бөледі, бірақ оларға маңызды өкілеттіктер берілген жағдайда. Мұндай бағдары бар адам кәсіпорынның әртүрлі аспектілерін басқаратын лауазымға келмейінше, мансаптық мақсатына жеткен жоқ деп есептейді."

            elif (
                    max_orientation == 'Стабильность работы: Стабильная, надежная работа на длительное времяЭти люди испытывают потребность в безопасности, защите и возможности прогнозирования и будут искать постоянную работу с минимальной вероятностью увольнения. Эти люди отождествляют свою работу со своей карьерой. Их потребность в безопасности и стабильности ограничивает выбор вариантов карьеры. Авантюрные или краткосрочные проекты и только становящиеся на ноги компании их, скорее всего, не привлекают. Они очень ценят социальные гарантии, которые может предложить работодатель, и, как правило, их выбор места работы связан именно с длительным контрактом и стабильным положением компании на рынке. Такие люди ответственность за управление своей карьерой перекладывают на нанимателя.'):
                max_orientation = "Жұмыс стабильділігі: Еңбекте ең бастысы – еркіндік пен тәуелсіздік. Бұл бағдары бар адамның басты мәселесі - ұйымдық ережелерден, ережелерден және шектеулерден құтылу. Олар белгіленген ережелерге, процедураларға, жұмыс уақытына, тәртіпке, киім үлгісіне және т.б. байланысты қиындықтарды бастан кешіреді. Олар жұмысты өз жолымен, өз қарқынымен және өз стандарттарына сай жасағанды ​​ұнатады. Олар жеке өміріне жұмыс кедергі болғанын ұнатпайды, сондықтан олар өз бетінше дербес мансаппен айналысуды жөн көреді. Олар автономия мен тәуелсіздіктен бас тартқанша, сапасыз жұмысты таңдағанды ​​жөн көреді. Олар үшін мансаптық дамудың бірінші кезектегі міндеті - өз бетінше жұмыс істеу мүмкіндігін алу, белгілі бір мақсаттарға жету үшін қалай, қашан және не істеу керектігін өздері шешу. Олар үшін мансап, ең алдымен, олардың еркіндігін жүзеге асырудың жолы, сондықтан кез келген шеңбер және қатаң бағыну оларды тіпті сыртқы тартымды бос орыннан да итермелейді. Мұндай адам жеткілікті еркіндік деңгейін қамтамасыз ететін ұйымда жұмыс істей алады."

            elif (max_orientation == "Стабильность места жительства"):
                max_orientation = "Тұрғын үй стабильділігі: Тұрақты, қауіпсіз, ұзақ мерзімді жұмыспен қамту Бұл адамдар қауіпсіздікке, қорғауға және болжамдылыққа мұқтаж және кету ықтималдығы аз болатын тұрақты жұмыс іздейді. Бұл адамдар өз жұмысын мансаппен сәйкестендіреді. Олардың қауіпсіздік пен тұрақтылыққа деген қажеттілігі олардың мансаптық мүмкіндіктерін шектейді. Олар, ең алдымен, шытырман оқиғалы немесе қысқа мерзімді жобаларға және аяққа тұрып жатқан компанияларға тартылмайды. Олар жұмыс беруші ұсына алатын әлеуметтік кепілдіктерді жоғары бағалайды және, әдетте, олардың жұмыс орнын таңдауы дәл ұзақ мерзімді келісімшартпен және компанияның нарықтағы тұрақты позициясымен байланысты. Мұндай адамдар мансапты басқару жауапкершілігін жұмыс берушіге жүктейді. Көбінесе бұл құндылық бағдары ұмтылыстың төмен деңгейімен үйлеседі."

            elif (
                    max_orientation == 'Служение Воплощать в работе свои идеалы и ценности. Данная ценностная ориентация характерна для людей, занимающихся делом по причине желания реализовать в своей работе главные ценности. Они часто ориентированы больше на ценности, чем на требующиеся в данном виде работы способности. Они стремятся приносить пользу людям, обществу, для них очень важно видеть конкретные плоды своей работы, даже если они и не выражены в материальном эквиваленте. Основной тезис построения их карьеры – получить возможность максимально эффективно использовать их таланты и опыт для реализации общественно важной цели. Люди, ориентированные на служение, общительны и часто консервативны. Человек с такой ориентацией не будет работать в организации, которая враждебна его целям и ценностям.'):
                max_orientation = "Қызмет: Ең бастысы - өз қалаңызда тұру (ең аз көшу, іссапарлар). Жаңа аймақта жоғарылату немесе жаңа жұмысқа орналасудан гөрі бір тұрғылықты жерінде қалу маңыздырақ. Көшіп-қону мұндай адамдар үшін қолайсыз, тіпті жиі іссапарлар жұмыс туралы ұсынысты қарастырған кезде олар үшін жағымсыз фактор болып табылады."

            elif (
                    max_orientation == 'Вызов: Сделать невозможное – возможным, решать уникальные задачи. Эти люди считают успехом преодоление непреодолимых препятствий, решение неразрешимых проблем или просто выигрыш. Они ориентированы на то, чтобы “бросать вызов”. Для одних людей вызов представляет более трудная работа, для других это — конкуренция и межличностные отношения. Они ориентированы на решение заведомо сложных задач, преодоление препятствий ради победы в конкурентной борьбе. Они чувствуют себя преуспевающими только тогда, когда постоянно вовлечены в решение трудных проблем или в ситуацию соревнования. Карьера для них – это постоянный вызов их профессионализму, и они всегда готовы его принять. Социальная ситуация чаще всего рассматривается с позиции “выигрыша – проигрыша”. Процесс борьбы и победа более важна для них, чем конкретная область деятельности или квалификация. Новизна,разнообразие и вызов имеют для них очень большую ценность, и, если все идет слишком просто, им становиться скучно.'):
                max_orientation = "Сын: Сіздің идеалдарыңыз бен құндылықтарыңызды жұмысыңызға енгізу. Бұл құндылық бағдары өз жұмысындағы негізгі құндылықтарды жүзеге асыруға деген ұмтылысының арқасында бизнеспен айналысатын адамдарға тән. Олар көбінесе белгілі бір жұмыс түріне қажетті қабілеттерге емес, құндылықтарға көбірек назар аударады. Олар адамдарға және қоғамға пайда келтіруге тырысады, олар үшін материалдық эквивалентте көрсетілмесе де, олардың жұмысының нақты жемісін көру өте маңызды. Олардың мансабын құрудың негізгі тезисі – әлеуметтік маңызды мақсатқа жету үшін өзінің таланты мен тәжірибесін барынша тиімді пайдалану мүмкіндігін алу. Қызмет көрсетуге бағытталған адамдар көпшіл және көбінесе консервативті. Мұндай бағдары бар адам өзінің мақсаттары мен құндылықтарына қарсы ұйымда жұмыс істемейді."

            elif (
                    max_orientation == 'Интеграция стилей жизни: Сохранение гармонии между сложившейся личной жизнью и карьерой. Для людей этой категории карьера должна ассоциироваться с общим стилем жизни, уравновешивая потребности человека, семьи и карьеры. Они хотят, чтобы организационные отношения отражали бы уважение к их личным и семейным проблемам. Выбирать и поддерживать определенный образ жизни для них важнее, чем добиваться успеха в карьере. Развитие карьеры их привлекает только в том случае, если она не нарушает привычный им стиль жизни и окружение. Для них важно, чтобы все было уравновешено – карьера, семья, личные интересы и т.п. Жертвовать чем-то одним ради другого им явно не свойственно. Такие люди обычно в своем поведении проявляют конформность (тенденция изменять свое поведение в зависимости от влияния других людей, с тем, чтобы оно соответствовало мнению окружающих)'):
                max_orientation = "Өмір салтын интеграциялау"

            elif (
                    max_orientation == 'Предпринимательство Создавать новые организации, товары, услуги. Этим людям нравится создавать новые организации, товары или услуги, которые могут быть отождествлены с их усилиями. Работать на других – это не их, они – предприниматели по духу, и цель их карьеры – создать что-то новое, организовать свое дело, воплотить в жизнь идею, всецело принадлежащую только им. Вершина карьеры в их понимании – собственный бизнес.'):
                max_orientation = "Кәсіпкерлік"

        new_result = TestResult.objects.create(
            user_data=user_data,
            test_name="Тест якоря карьеры",
            result=max_orientation
        )

        domain = 'https://gasyrfoundation.com'
        admin_change_path = reverse('admin:test_app_testresult_change', args=(new_result.id,))
        admin_url = f"{domain}{admin_change_path}"
        whatsapp_message = f"Привет, вот ссылка на результат / Сәлем, нәтижеге сілтеме: {admin_url}"
        encoded_whatsapp_message = quote(whatsapp_message)
        whatsapp_link = f"https://wa.me/77000660868?text={encoded_whatsapp_message}"

        return render(request, 'test_app/career_anchor_results.html', {
            'max_orientation': max_orientation,
            'text1': "Результаты закрепления вашей карьеры" if language == "RU" else "Сіздің мансабыңызды бекіту нәтижелері",
            'text2': "Ваша доминирующая карьерная ориентация - это:" if language == "RU" else "Сіздің басым мансаптық бағдарыңыз:",
            'user_data_id': user_data_id,
            'submit_text': submit_text,
            'whatsapp_link': whatsapp_link
        })

    return render(request, 'test_app/career_anchor_test.html', {
        'form': form,
        'user_data_id': user_data_id,
        'submit_text': submit_text
    })


from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

def send_admin_result_via_whatsapp(request, result_id):
    # Ensure you have the correct result_id being passed to the view
    result = get_object_or_404(TestResult, pk=result_id)

    # Construct the admin URL for this specific result
    admin_url = f"http://127.0.0.1:8000/admin/test_app/testresult/{result.id}/change/"

    # Construct the WhatsApp URL
    whatsapp_message = f"Привет, вот ссылка на результат / Сәлем, нәтижеге сілтеме: {admin_url}"
    whatsapp_link = f"https://wa.me/77000660868?text={whatsapp_message}"

    # You could also return this link to a template to show a clickable link/button
    return HttpResponseRedirect(whatsapp_link)

from django.http import HttpResponse


def oprosnik_view(request, user_data_id):
    user_data = get_object_or_404(UserData, id=user_data_id)
    language = user_data.language
    if request.method == 'POST':


        if language == "KZ":
            form = Oprosnik_kk(request.POST)
        else:
            form = Oprosnik(request.POST)

        if form.is_valid():
            # Собираем данные из формы
            data = {
                'Первый вопрос': form.cleaned_data['question_1'],
                'Второй вопрос': form.cleaned_data['question_2'],
                'Третий вопрос': form.cleaned_data['question_3'],
            }
            # Создаем запись в базе данных

            TestResult.objects.create(user_data_id=user_data_id, test_name="Опросник", result=str(data))

            return redirect('home', user_data_id=user_data.id)
    else:
        if language == "KZ":
            form = Oprosnik_kk(request.POST)
        else:
            form = Oprosnik(request.POST)
    return render(request, 'test_app/oprosnik.html', {'form': form})