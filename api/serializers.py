from rest_framework import serializers
from .models import Profile, Matching


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "user",
            "user_sex",
            "user_name",
            "user_age",
            "user_mbti_1",
            "user_mbti_2",
            "user_mbti_3",
            "user_mbti_4",
            "user_school",
            "user_kakaoid",
            "user_password",
            "want_age_min",
            "want_age_max",
            "want_mbti",
        )

class MatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matching
        fields = ("user", "matched_list", "ok_list", "no_list", "final_matching", "last_matching_time")