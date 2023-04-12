from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from immigration.models import UserSurvey

# Create your views here.

class UserSurveyCreate(CreateView):
    model = UserSurvey
    # 모델이름_form.html 에 연결 (모델이름 소문자!)
    fields = "__all__" # ['first_name', 'last_name', ... ]
    success_url = reverse_lazy('immigration:thankyou')

def thankyou_view(request):
    return render(
        request,
        'thankyou.html',
    )