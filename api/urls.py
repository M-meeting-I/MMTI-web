from django.urls import path
from .views import ProfileList, ProfileDetail, MatchingList, MatchingDetail


urlpatterns = [
    path('profile/', ProfileList.as_view()),
    path('profile/<int:user>/', ProfileDetail.as_view()),
    path('matching/', MatchingList.as_view()),
    path('matching/<int:user>/', MatchingDetail.as_view()),
]