from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class UserSurvey(models.Model):
    user_sex = models.BooleanField()
    user_name = models.CharField(max_length=5)
    user_age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)])

    user_mbti_1 = models.CharField(max_length=5)
    user_mbti_2 = models.CharField(max_length=5)
    user_mbti_3 = models.CharField(max_length=5)
    user_mbti_4 = models.CharField(max_length=5)

    user_school = models.CharField(max_length=20)
    user_image = models.ImageField(upload_to='immigration/images/%Y/%m/%d/')
    user_kakaoid = models.CharField(max_length=40)

    want_age_min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)])
    want_age_max = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)])

    want_mbti_1 = models.CharField(max_length=5)
    want_mbti_2 = models.CharField(max_length=5)
    want_mbti_3 = models.CharField(max_length=5)
    want_mbti_4 = models.CharField(max_length=5)

    user_survey_at = models.DateTimeField(auto_now_add=True)