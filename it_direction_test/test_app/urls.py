from django.urls import path
from .views import *

urlpatterns = [
    path('test/<int:user_data_id>/', test_view, name='test_view'),
    path('holland_test/<int:user_data_id>/', holland_test_view , name='holland_test'),
    path('preference-test/<int:user_data_id>/', preference_test_view, name='preference_test'),
    path('map-test/<int:user_data_id>/', survey_view, name='survey'),
    path('career-anchor-test/<int:user_data_id>/', career_anchor_test_view, name='career_anchor_test'),
    path('', collect_user_data_view, name='collect_user_data_view'),
    path('home/<int:user_data_id>/', index,name = "home")
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
