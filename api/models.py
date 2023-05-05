from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Matching(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    matched_list = models.TextField()
    last_matching_time = models.DateTimeField(auto_now=True)
    ok_list = models.TextField(null=True, blank=True)
    final_matching = models.TextField(null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)

    user_sex = models.BooleanField()
    user_name = models.CharField(max_length=5)
    user_age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)])

    # "xxxox" 형식
    user_mbti_1 = models.CharField(max_length=5)
    user_mbti_2 = models.CharField(max_length=5)
    user_mbti_3 = models.CharField(max_length=5)
    user_mbti_4 = models.CharField(max_length=5)

    user_school = models.CharField(max_length=20)
    user_image = models.ImageField(upload_to='immigration/images/%Y/%m/%d/', null=True, blank=True)
    user_kakaoid = models.CharField(max_length=40)
    user_password = models.CharField(max_length=20)

    want_age_min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)])
    want_age_max = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)])

    # "enfp,entj,infp" 형식
    want_mbti = models.CharField(max_length=80)

    user_survey_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        self.is_male = "여자"
        if self.user_sex:
            self.is_male = "남자"
        return f'{self.user_name} {self.user_age} {self.is_male}'
    
    def get_user_mbti(self):
        mbti = list()
        for i in range(5):
            if self.user_mbti_1[i] == "o":
                if i <= 1:
                    mbti.append('e')
                elif i == 2:
                    mbti.append('x')
                else:
                    mbti.append('i')
        for i in range(5):
            if self.user_mbti_2[i] == "o":
                if i <= 1:
                    mbti.append('n')
                elif i == 2:
                    mbti.append('x')
                else:
                    mbti.append('s')
        for i in range(5):
            if self.user_mbti_3[i] == "o":
                if i <= 1:
                    mbti.append('f')
                elif i == 2:
                    mbti.append('x')
                else:
                    mbti.append('t')
        for i in range(5):
            if self.user_mbti_4[i] == "o":
                if i <= 1:
                    mbti.append('p')
                elif i == 2:
                    mbti.append('x')
                else:
                    mbti.append('j')
        result = "".join(mbti)
        return result