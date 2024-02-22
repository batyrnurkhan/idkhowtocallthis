from django.urls import path
from . import views
from .views import holland_test, UserDataView

urlpatterns = [
    path('first-test', views.test_view, name='test_view'),
    path('holland-test/', holland_test, name='holland_test'),
    path('', UserDataView.as_view(), name='userdata'),
]
