from django.urls import path
from .views import ProfileList, ProfileDetail


urlpatterns = [
    path('profile/', ProfileList.as_view()),
    path('profile/<int:user>/', ProfileDetail.as_view()),
]