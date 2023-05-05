from django.db.models import Q
from django.contrib.auth.models import User
from .models import Profile, Matching

import json

def age_check(user):
    result = Profile.objects.filter(~Q(user_sex=user.user_sex)
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
                result.append(target.user.pk)
                break
    
    return result


def Q_pid(profile):
    
    # 나이 필터
    age_result = age_check(profile)
    # mbti 필터
    mbti_result = mbti_check(profile, age_result)
    # 적합자 리스트 저장

    # profile : 대상자의 Profile , mbti_result : 매칭된 User.pk 리스트
    
    obj, created = Matching.objects.update_or_create(user=profile.user, defaults={'matched_list': json.dumps(mbti_result)})
    obj.save()
    
    me_pk = profile.user.pk
    for i in mbti_result:
        target = User.objects.get(pk=i)
        old_list = json.loads(target.matching.matched_list)
        if me_pk in old_list:
            pass
        else:
            old_list.append(me_pk)
            target.matching.matched_list = json.dumps(old_list)
            target.matching.save()
