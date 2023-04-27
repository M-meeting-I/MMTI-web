
from django.shortcuts import render
from immigration.models import UserSurvey
from django.db.models import Q



def age_check(user):
    result = UserSurvey.objects.filter(~Q(user_sex=user.user_sex)
                                       & Q(user_age__gte=user.want_age_min)
                                       & Q(user_age__lte=user.want_age_max)
                                       & Q(want_age_min__lte=user.user_age)
                                       & Q(want_age_max__gte=user.user_age)).all()
    return result

def mbti_check(user, age_set):
    result = list()

    # want_mbti_list = ['enfp', 'infj', 'istj']
    want_mbti_str = user.want_mbti
    want_mbti_str = want_mbti_str.strip()
    want_mbti_list = want_mbti_str.split(',')
    for i in want_mbti_list:
        i = i.strip()

    # target 에 대해 for문을 돌리고 적합하면 result에 append
    for target in age_set:
        
        target_mbti = target.get_user_mbti()
        for mbti in want_mbti_list:
            is_correct = True
            for i in range(4):
                if target_mbti[i] == "x":
                    continue
                elif mbti[i] != target_mbti[i]:
                    is_correct = False
            if is_correct == False:
                continue
            else:
                result.append(target)
                break
    
    return result


def Q_pid(user):
    # 나이 필터
    age_result = age_check(user)
    # mbti 필터
    mbti_result = mbti_check(user, age_result)
    # 적합자 리스트 저장
    # pk_list = []
    # for i in mbti_result:
    #     pk_list.append(i.pk)

    # user.Q_pid_list = json.dumps(pk_list)

    for i in mbti_result:
        u = i.user_model
        user.object.Q_pid_list.add(u)

    user.save()


def matching_render(request):
    
    male_set = UserSurvey.objects.filter(user_sex=True).all()
    context = dict()

    for i in male_set:
        Q_pid(i)
        context[i.pk] = i.Q_pid_list.all().username

    return render(
        request,
        'immigration/result_page.html',
        {
            'result': context
        }
    )