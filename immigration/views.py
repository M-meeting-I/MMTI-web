from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from immigration.models import UserSurvey
from django.http import HttpResponse
from django.db.models import Q
import json

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

def age_check(user):
    result = UserSurvey.objects.filter(~Q(user_sex=user.user_sex)
                                       & Q(user_age__gte=user.want_age_min)
                                       & Q(user_age__lte=user.want_age_max)
                                       & Q(want_age_min__lte=user.user_age)
                                       & Q(want_age_max__gte=user.user_age)).all()
    return result

def mbti_check(user, age_set) -> list:
    # age_set : 나이 필터 거치고 난 뒤 사람들 집합

    result = [] # mbti 필터 거치고 난 뒤 사람들 넣을 리스트

    for target in age_set:
        # is_correct_1=True -> user가 원하는 첫 번째 mbti(E,I)와 target의 첫 번째 mbti 일치
        is_correct_1 = is_correct_2 = is_correct_3 = is_correct_4 = False
        # metoo_correct_1=True -> target이 원하는 첫 번째 mbti와 user의 첫 번째 mbti 일치
        metoo_correct_1 = metoo_correct_2 = metoo_correct_3 = metoo_correct_4 = False

        # ---------- E, I ----------
        for i in range(5):
            if (user.want_mbti_1[i] == "o" and target.user_mbti_1[i] == "o"):
                is_correct_1 = True
            if (target.want_mbti_1[i] == "o" and user.user_mbti_1[i] == "o"):
                metoo_correct_1 = True
            if (is_correct_1 and metoo_correct_1):
                break
        if (is_correct_1 == False or metoo_correct_1 == False): # 첫 번째 mbti 부적합이므로 continue로 다음 사람으로 건너뜀
            continue

        # ---------- N, S ----------
        for i in range(5):
            if (user.want_mbti_2[i] == "o" and target.user_mbti_2[i] == "o"):
                is_correct_2 = True
            if (target.want_mbti_2[i] == "o" and user.user_mbti_2[i] == "o"):
                metoo_correct_2 = True
            if (is_correct_2 and metoo_correct_2):
                break
        if (is_correct_2 == False or metoo_correct_2 == False): # 두 번째 mbti 부적합이므로 continue로 다음 사람으로 건너뜀
            continue

        # ---------- F, T ----------
        for i in range(5):
            if (user.want_mbti_3[i] == "o" and target.user_mbti_3[i] == "o"):
                is_correct_3 = True
            if (target.want_mbti_3[i] == "o" and user.user_mbti_3[i] == "o"):
                metoo_correct_3 = True
            if (is_correct_3 and metoo_correct_3):
                break
        if (is_correct_3 == False or metoo_correct_3 == False): # 세 번째 mbti 부적합이므로 continue로 다음 사람으로 건너뜀
            continue

        # ---------- P, J ----------
        for i in range(5):
            if (user.want_mbti_4[i] == "o" and target.user_mbti_4[i] == "o"):
                is_correct_4 = True
            if (target.want_mbti_4[i] == "o" and user.user_mbti_4[i] == "o"):
                metoo_correct_4 = True
            if (is_correct_4 and metoo_correct_4):
                break
        if (is_correct_4 == False or metoo_correct_4 == False): # 네 번째 mbti 부적합이므로 continue로 다음 사람으로 건너뜀
            continue

        result.append(target) # 리스트에 추가
    
    return result

def Q_pid(user):
    # 나이 필터
    age_result = age_check(user)
    # mbti 필터
    mbti_result = mbti_check(user, age_result)
    # 적합자 리스트 저장
    pk_list = []
    for i in mbti_result:
        pk_list.append(i.pk)

    user.Q_pid_list = json.dumps(pk_list)
    user.save()
    return mbti_result


def matching_render(request):
    youyou = UserSurvey.objects.get(user_name='심규원')
    result = Q_pid(youyou)

    return render(
        request,
        'immigration/result_page.html',
        {
            'result':result,
        }
    )