from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin
from import_export import resources
from import_export.fields import Field

class TestResultResource(resources.ModelResource):
    user_full_name = Field()  # This will hold the concatenated full name

    class Meta:
        model = TestResult
        fields = ('id', 'user_full_name', 'test_name', 'result', 'created_at')  # Including the new field
        export_order = ('id', 'user_full_name', 'test_name', 'result', 'created_at')

    def dehydrate_user_full_name(self, test_result):
        # This method will be called to fill the 'user_full_name' field
        return f"{test_result.user_data.first_name} {test_result.user_data.last_name}"
class UserDataResource(resources.ModelResource):
    full_name = Field(attribute='full_name', column_name='Full Name')

    class Meta:
        model = UserData
        fields = ('email', 'phone_number', 'full_name')  # Specify fields here
        export_order = ('full_name', 'email', 'phone_number')

    def dehydrate_full_name(self, user_data):
        return f"{user_data.first_name} {user_data.last_name}"
@admin.register(UserData)
class UserDataAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = UserDataResource
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Other Details', {'fields': ('language', 'grade', 'parent_first_name', 'parent_last_name', 'parent_phone_number')}),
    )

@admin.register(TestResult)
class TestResultAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = TestResultResource  # Using the custom resource class
    list_display = ('user_data', 'test_name', 'result', 'created_at')
    list_filter = ('test_name', 'created_at')
    search_fields = ('user_data__first_name', 'user_data__last_name', 'test_name')

@admin.register(Question)
class QuestionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text', 'choice_a', 'choice_b')

@admin.register(Question_kk)
class QuestionKkAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text', 'choice_a', 'choice_b')

  # Fields to display in the admin list view

# Register the models with their respective admin classes
@admin.register(HollandQuestion)
class HollandQuestionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('text', 'choice_a', 'choice_b')  # Fields to display in the admin list view

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

admin.site.register(CareerAnchorResponse)