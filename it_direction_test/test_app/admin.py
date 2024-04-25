from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin

@admin.register(UserData)
class UserDataAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Other Details', {'fields': ('language', 'grade', 'parent_first_name', 'parent_last_name', 'parent_phone_number')}),
    )

@admin.register(TestResult)
class TestResultAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('user_data', 'test_name', 'result', 'created_at')
    list_filter = ('test_name', 'created_at')
    search_fields = ('user_data__first_name', 'user_data__last_name', 'test_name')

admin.site.register(MapQuestion_kk)
admin.site.register(MapQuestion)

admin.site.register(Question)
admin.site.register(Question_kk)

admin.site.register(PreferenceQuestion)
admin.site.register(PreferenceQuestion_kk)

admin.site.register(HollandQuestion)
admin.site.register(HollandQuestion_kk)

admin.site.register(CareerAnchorQuestion)
admin.site.register(CareerAnchorQuestion_kk)
admin.site.register(CareerAnchorResponse)