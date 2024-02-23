from django.urls import path
from .views import *

urlpatterns = [
    path('test/<int:user_data_id>/', test_view, name='test_view'),
    path('holland_test/<int:user_data_id>/', holland_test, name='holland_test'),
    path('preference-test/<int:user_data_id>/', preference_test_view, name='preference_test'),
    path('map-test/<int:user_data_id>/', survey_view, name='survey'),
    path('career-anchor-test/<int:user_data_id>/', career_anchor_test_view, name='career_anchor_test'),
    path('home/<int:user_data_id>/', index, name='home'),  # 'home' is the URL name for home_view

    # path('home<int:user_data_id>/', home_view, name='home'),
    path('', collect_user_data_view, name='collect_user_data_view'),
]
