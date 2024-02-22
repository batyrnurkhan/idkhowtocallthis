from django.contrib import admin
from .models import Question, HollandQuestion, UserData

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text']

@admin.register(HollandQuestion)
class HollandQuestionAdmin(admin.ModelAdmin):
    list_display = ['text']

admin.site.register(UserData)