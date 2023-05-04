from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.db.models import Q

from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import ProfileSerializer
from .models import Profile


# Create your views here.

class ProfileList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            profile.user = User.objects.create_user(username=serializer.data['user_kakaoid'], password=serializer.data['user_password'])
            profile.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
                result.append(target)
                break
    
    return result


def Q_pid(user):
    # 나이 필터
    age_result = age_check(user)
    # mbti 필터
    mbti_result = mbti_check(user, age_result)
    # 적합자 리스트 저장
    for i in mbti_result:
        u = i.user_model
        user.Q_pid_list.add(u)

    user.save()


def matching_render(request):
    
    male_set = Profile.objects.filter(user_sex=True).all()
    context = dict()

    for i in male_set:
        li = []
        Q_pid(i)
        for j in i.Q_pid_list.all():
            li.append(j.username)
        context[i.pk] = li

    return render(
        request,
        'immigration/result_page.html',
        {
            'result': context
        }
    )