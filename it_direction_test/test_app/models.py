from django.db import models


class UserData(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    language = models.CharField(max_length=2, choices=(('RU', 'Russian'), ('KZ', 'Kazakh')))

    # New fields
    GRADE_CHOICES = [(i, str(i)) for i in range(1, 13)]  # Generates pairs of grade numbers for choices
    grade = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True, default=None)
    parent_first_name = models.CharField(max_length=100, default='', blank=True)
    parent_last_name = models.CharField(max_length=100, default='', blank=True)
    parent_phone_number = models.CharField(max_length=100, default='', blank=True)

    CITY_CHOICES = [
        ('Almaty', 'Алматы'),
        ('Astana', 'Астана'),
        ('Shymkent', 'Шымкент'),

    ]
    city = models.CharField(max_length=50, choices=CITY_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'Данные клиента'
        verbose_name_plural = 'Данные клиентов'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Question(models.Model):
    text = models.CharField(max_length=1024)
    choice_a = models.CharField(max_length=512)
    choice_b = models.CharField(max_length=512)

    class Meta:
        verbose_name = '1. Тест-опросник на профориентацию | Вопрос и ответы'
        verbose_name_plural = '1. Тест-опросник на профориентацию | Вопросы и ответы'

    def __str__(self):
        return f'{self.text} - {self.choice_a} - {self.choice_b}'

class Question_kk(models.Model):
    text = models.CharField(max_length=1024)
    choice_a = models.CharField(max_length=512)
    choice_b = models.CharField(max_length=512)

    class Meta:
        verbose_name = '1. Тест-опросник на профориентацию | сұрақтар және жауабтар'
        verbose_name_plural = '1. Тест-опросник на профориентацию | сұрақтары және жауабтары'

    def __str__(self):
        return f'{self.text} - {self.choice_a} - {self.choice_b}'

class HollandQuestion(models.Model):
    text = models.CharField(max_length=1024, default='Из каждой пары профессий нужно указать одну, предпочитаемую')
    choice_a = models.CharField(max_length=512)
    choice_b = models.CharField(max_length=512)


    class Meta:
        verbose_name = '2. Тест-опросник на определение типа личности | Вопрос и ответы'
        verbose_name_plural = '2. Тест-опросник на определение типа личности |Вопросы ответы второго теста'

    def __str__(self):
        return f"Question {self.id}"


class HollandQuestion_kk(models.Model):
    text = models.CharField(max_length=1024, default='Из каждой пары профессий нужно указать одну, предпочитаемую')
    choice_a = models.CharField(max_length=512)
    choice_b = models.CharField(max_length=512)

    class Meta:
        verbose_name = '2. Тұлға түрін анықтауға арналған тест-сауалнама | сұрағы және жауабы'
        verbose_name_plural = '2. Тұлға түрін анықтауға арналған тест-сауалнама | сұрақтары және жауабтары'

    def __str__(self):
        return f"Question {self.id}"

class PreferenceQuestion(models.Model):
    text = models.CharField(max_length=1024)
    option_a = models.CharField(max_length=512)
    option_b = models.CharField(max_length=512)

    class Meta:
        verbose_name = '3. Тест на профессиональные предпочтения | Вопрос и ответ'
        verbose_name_plural = '3. Тест на профессиональные предпочтения | Вопросы и ответы'

    def __str__(self):
        return self.text

class PreferenceQuestion_kk(models.Model):
    text = models.CharField(max_length=1024)
    option_a = models.CharField(max_length=512)
    option_b = models.CharField(max_length=512)

    class Meta:
        verbose_name = '3. Кәсіби артықшылық сынағы | сұрағы және жауабтары'
        verbose_name_plural = '3. Кәсіби артықшылық сынағы | сұрақтары және жауабтары'

    def __str__(self):
        return self.text


class CareerAnchorQuestion(models.Model):
    text = models.CharField(max_length=1024)
    class Meta:
        verbose_name = '4. Тест "Якоря карьеры" | Вопрос'
        verbose_name_plural = '4. Тест "Якоря карьеры" | Вопросы'
    def __str__(self):
        return self.text

class CareerAnchorQuestion_kk(models.Model):
    text = models.CharField(max_length=1024)

    class Meta:
        verbose_name = '4. "Мансап зәкірі" тесті | сұрағы'
        verbose_name_plural = '4. "Мансап зәкірі"тесті | сұрақтары'

    def __str__(self):
        return self.text

class CareerAnchorResponse(models.Model):
    question = models.ForeignKey(CareerAnchorQuestion, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name = '4. Тест "Якоря карьеры" | Вопрос и ответ'
        verbose_name_plural = '4. Тест "Якоря карьеры" | Вопросы и ответы'

    def __str__(self):
        return self.question

class TestResult(models.Model):
    user_data = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='test_results')
    test_name = models.CharField(max_length=100)
    result = models.TextField()  # You can adjust the fields based on the type of result you need to store
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'

    def __str__(self):
        return f"{self.test_name} result for {self.user_data}"





