from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin


@admin.register(UserData)
class UserDataAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'city')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('city',)
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Other Details',
         {'fields': ('language', 'grade', 'parent_first_name', 'parent_last_name', 'parent_phone_number')}),
    )


@admin.register(TestResult)
class TestResultAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('user_data', 'test_name', 'result', 'created_at')
    list_filter = ('test_name', 'created_at')
    search_fields = ('user_data__first_name', 'user_data__last_name', 'test_name')


@admin.register(Question)
class QuestionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text', 'choice_a', 'choice_b')


@admin.register(Question_kk)
class QuestionKkAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text', 'choice_a', 'choice_b')


@admin.register(HollandQuestion)
class HollandQuestionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text', 'choice_a', 'choice_b')


@admin.register(HollandQuestion_kk)
class HollandQuestionKkAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text', 'choice_a', 'choice_b')


@admin.register(PreferenceQuestion)
class PreferenceQuestionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text', 'option_a', 'option_b')


@admin.register(PreferenceQuestion_kk)
class PreferenceQuestionKkAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text', 'option_a', 'option_b')


@admin.register(CareerAnchorQuestion)
class CareerAnchorQuestionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text',)


@admin.register(CareerAnchorQuestion_kk)
class CareerAnchorQuestionKkAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text',)

