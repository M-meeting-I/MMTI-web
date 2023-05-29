from django.db.models import Q
from django.contrib.auth.models import User
from .models import Profile, Matching

from haversine import haversine
import json

def age_check(user):
    result = Profile.objects.filter(~Q(user_sex=user.user_sex) 
                                    & Q(is_active=True)
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

def match_to_inactive(profile):
    m_li = profile.user.matching.matched_list
    if m_li != "[]":
        profile.is_active = False

def cal_score(profile_1, profile_2):
    # 두 사람의 프로필을 받아서 두 사람 사이의 매칭 스코어를 계산하는 코드
    score = 0
    # 나이 고려
    score += 400 - (abs(profile_1.user_age - profile_2.user_age) * 50)
    # 거주지 고려
    latlog = {"강남구" : (37.514575, 127.0495556),
              "강동구" : (37.52736667, 127.1258639),
              "강북구" : (37.63695556, 127.0277194),
              "강서구" : (37.54815556, 126.851675),
              "관악구" : (37.47538611, 126.9538444),
              "광진구" : (37.53573889, 127.0845333),
              "구로구" : (37.49265, 126.8895972),
              "금천구" : (37.44910833, 126.9041972),
              "노원구" : (37.65146111, 127.0583889),
              "도봉구" : (37.66583333, 127.0495222),
              "동대문구" : (37.571625, 127.0421417),
              "동작구" : (37.50965556, 126.941575),
              "마포구" : (37.56070556, 126.9105306),
              "서대문구" : (37.57636667, 126.9388972),
              "서초구" : (37.48078611, 127.0348111),
              "성동구" : (37.56061111, 127.039),
              "성북구" : (37.58638333, 127.0203333),
              "송파구" : (37.51175556, 127.1079306),
              "양천구" : (37.51423056, 126.8687083),
              "영등포구" : (37.52361111, 126.8983417),
              "용산구" : (37.53609444, 126.9675222),
              "은평구" : (37.59996944, 126.9312417),
              "종로구" : (37.57037778, 126.9816417),
              "중구" : (37.56100278, 126.9996417),
              "중랑구" : (37.60380556, 127.0947778),
              }
    place_1 = latlog[profile_1.user_residence]
    place_2 = latlog[profile_2.user_residence]
    distance = haversine(place_1, place_2, unit='km')
    score += 400 - distance
    
    return score
    


def matching_sort(matching):
    # matching : Matching 오브젝트
    before_list = json.loads(matching.matched_list)
    
    # 여기에 점수순으로 정렬하는 코드



def Q_pid(profile):
    
    # 나이 필터
    age_result = age_check(profile)
    # mbti 필터
    mbti_result = mbti_check(profile, age_result)
    # 적합자 리스트 저장

    # profile : 대상자의 Profile , mbti_result : 매칭된 User.pk 리스트
    
    obj, created = Matching.objects.update_or_create(user=profile.user, defaults={'matched_list': json.dumps(mbti_result)})
    obj.save()
    match_to_inactive(profile)
    
    # 상대의 matched_list 업데이트
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
        match_to_inactive(target.profile)
