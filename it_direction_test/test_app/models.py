from django.db import models
class UserData(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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

class PreferenceQuestion(models.Model):
    text = models.CharField(max_length=1024)
    option_a = models.CharField(max_length=512)
    option_b = models.CharField(max_length=512)

    def __str__(self):
        return self.text

class MapQuestion(models.Model):
    text = models.TextField()


class MapQuestion_kk(models.Model):
    text = models.TextField()

class CareerAnchorQuestion(models.Model):
    text = models.CharField(max_length=1024)
    # Since your test uses a rating scale from 1 to 10, no need for choice fields

    def __str__(self):
        return self.text

class CareerAnchorResponse(models.Model):
    question = models.ForeignKey(CareerAnchorQuestion, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

class TestResult(models.Model):
    user_data = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='test_results')
    test_name = models.CharField(max_length=100)
    result = models.TextField()  # You can adjust the fields based on the type of result you need to store
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name} result for {self.user_data}"

