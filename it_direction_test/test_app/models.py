from django.db import models
from django.db import models

class UserData(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

class TestResult(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)  # Assuming the result will be stored as text

class Question(models.Model):
    text = models.CharField(max_length=1024)
    choice_a = models.CharField(max_length=512)
    choice_b = models.CharField(max_length=512)

    def __str__(self):
        return self.text

class HollandQuestion(models.Model):
    text = models.CharField(max_length=1024, default='Из каждой пары профессий нужно указать одну, предпочитаемую')
    choice_a = models.CharField(max_length=512)
    choice_b = models.CharField(max_length=512)

    def __str__(self):
        return f"Question {self.id}"