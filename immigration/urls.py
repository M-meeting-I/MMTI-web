from django.urls import path
from .views import UserSurveyCreate, thankyou_view

app_name = 'immigration'

urlpatterns = [
    path('', UserSurveyCreate.as_view(), name='survey'),
    path('thankyou/', thankyou_view, name='thankyou'),
]
