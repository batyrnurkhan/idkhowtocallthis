from django.contrib import admin
from .models import *
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text']

@admin.register(Question_kk)
class Question_kkAdmin(admin.ModelAdmin):
    list_display = ['text']

@admin.register(HollandQuestion)
class HollandQuestionAdmin(admin.ModelAdmin):
    list_display = ['text']

@admin.register(HollandQuestion_kk)
class HollandQuestion_kkAdmin(admin.ModelAdmin):
    list_display = ['text']
@admin.register(PreferenceQuestion)
class PreferenceQuestionAdmin(admin.ModelAdmin):
    list_display = ['text']

@admin.register(PreferenceQuestion_kk)
class PreferenceQuestion_kkAdmin(admin.ModelAdmin):
    list_display = ['text']

@admin.register(MapQuestion)
class MapQuestionAdmin(admin.ModelAdmin):
    list_display = ['text']
@admin.register(MapQuestion_kk)
class MapQuestionAdmin_kk(admin.ModelAdmin):
    list_display = ['text']

@admin.register(CareerAnchorQuestion)
class CareerAnchorQuestionAdmin(admin.ModelAdmin):
    list_display = ['text']

@admin.register(CareerAnchorQuestion_kk)
class CareerAnchorQuestion_kkAdmin(admin.ModelAdmin):
    list_display = ['text']

from django.contrib import admin
from .models import UserData, TestResult

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user_data', 'test_name', 'result', 'created_at')
    list_filter = ('test_name', 'created_at')
    search_fields = ('user_data__first_name', 'user_data__last_name', 'test_name')

