from django.db import models
class UserData(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    language = models.CharField(max_length=2, choices=(('RU', 'Russian'), ('KZ', 'Kazakh')))

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
        verbose_name = 'Вопрос и ответы первого теста'
        verbose_name_plural = 'Вопросыи ответы первого теста'

    def __str__(self):
        return f'{self.text} - {self.choice_a} - {self.choice_b}'

class Question_kk(models.Model):
    text = models.CharField(max_length=1024)
    choice_a = models.CharField(max_length=512)
    choice_b = models.CharField(max_length=512)

    class Meta:
        verbose_name = 'Бірінші тесттің сұрағы және жауабтары'
        verbose_name_plural = 'Бірінші тесттің сұрақтары және жауабтары'

    def __str__(self):
        return f'{self.text} - {self.choice_a} - {self.choice_b}'

class HollandQuestion(models.Model):
    text = models.CharField(max_length=1024, default='Из каждой пары профессий нужно указать одну, предпочитаемую')
    choice_a = models.CharField(max_length=512)
    choice_b = models.CharField(max_length=512)


    class Meta:
        verbose_name = 'Вопрос и ответы второго теста'
        verbose_name_plural = 'Вопросы ответы второго теста'

    def __str__(self):
        return f"Question {self.id}"


class HollandQuestion_kk(models.Model):
    text = models.CharField(max_length=1024, default='Из каждой пары профессий нужно указать одну, предпочитаемую')
    choice_a = models.CharField(max_length=512)
    choice_b = models.CharField(max_length=512)

    class Meta:
        verbose_name = 'Екінші тесттің сұрағы және жауабтары'
        verbose_name_plural = 'Екінші тесттің сұрақтары және жауабтары'

    def __str__(self):
        return f"Question {self.id}"

class PreferenceQuestion(models.Model):
    text = models.CharField(max_length=1024)
    option_a = models.CharField(max_length=512)
    option_b = models.CharField(max_length=512)

    class Meta:
        verbose_name = 'Вопрос и ответы третьего теста'
        verbose_name_plural = 'Вопросы ответы третьего теста'

    def __str__(self):
        return self.text

class PreferenceQuestion_kk(models.Model):
    text = models.CharField(max_length=1024)
    option_a = models.CharField(max_length=512)
    option_b = models.CharField(max_length=512)

    class Meta:
        verbose_name = 'Үшінші тесттің сұрағы және жауабтары'
        verbose_name_plural = 'Үшінші тесттің сұрақтары және жауабтары'

    def __str__(self):
        return self.text

class MapQuestion(models.Model):
    text = models.TextField()
    language = models.CharField(max_length=2, choices=(('RU', 'Russian'), ('KZ', 'Kazakh')), default=('RU', 'Russian'))

    class Meta:
        verbose_name = 'Вопрос и ответы четвертого теста'
        verbose_name_plural = 'Вопросы ответы четвертого теста'

    def __str__(self):
        return self.text



class MapQuestion_kk(models.Model):
    text = models.TextField()

    class Meta:
        verbose_name = 'Төртінші тесттің сұрағы және жауабтары'
        verbose_name_plural = 'Төртінші тесттің сұрақтары және жауабтары'

class CareerAnchorQuestion(models.Model):
    text = models.CharField(max_length=1024)
    class Meta:
        verbose_name = 'Вопрос пятого теста'
        verbose_name_plural = 'Вопросы пятого теста'
    def __str__(self):
        return self.text

class CareerAnchorQuestion_kk(models.Model):
    text = models.CharField(max_length=1024)

    class Meta:
        verbose_name = 'Алтыншы тесттің сұрағы'
        verbose_name_plural = 'Алтыншы тесттің сұрақтары'

    def __str__(self):
        return self.text

class CareerAnchorResponse(models.Model):
    question = models.ForeignKey(CareerAnchorQuestion, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Вопрос и ответ шестого теста'
        verbose_name_plural = 'Вопросы и ответы шестого теста'

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

