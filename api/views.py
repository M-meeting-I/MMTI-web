from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from rest_framework import status, mixins, generics
from rest_framework.response import Response

from .serializers import ProfileSerializer, MatchingSerializer
from .models import Profile, Matching
from .alg import Q_pid


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
            profile.user = User.objects.create_user(
                username=serializer.data['user_kakaoid'],
                password=serializer.data['user_password'])
            profile.save()
            Q_pid(profile)
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

    def put(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            Q_pid(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class MatchingDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     generics.GenericAPIView):
    queryset = Matching.objects.all()
    serializer_class = MatchingSerializer
    lookup_field = 'user'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class MatchingList(mixins.ListModelMixin,
                   generics.GenericAPIView):
    queryset = Matching.objects.all()
    serializer_class = MatchingSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)