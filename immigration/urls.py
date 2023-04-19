from django.urls import path
from .views import UserSurveyCreate, thankyou_view, matching_render

app_name = 'immigration'

urlpatterns = [
    path('', UserSurveyCreate.as_view(), name='survey'),
    path('thankyou/', thankyou_view, name='thankyou'),
    path('result/', matching_render, name='result'),
]
