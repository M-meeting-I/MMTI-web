from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile
from bs4 import BeautifulSoup

# Create your tests here.
class TestView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user_q1 = User.objects.create_user(username='shimq1', password='somepassword')
        self.user_joy = User.objects.create_user(username='조이', password='somepassword')
        self.user_wendy = User.objects.create_user(username='웬디', password='somepassword')
        

        self.user_male_001 = Profile.objects.create(
            user_model=self.user_q1,
            user_sex=True,
            user_name='심규원',
            user_age=21,
            user_mbti_1='xxxxo',
            user_mbti_2='xxxox',
            user_mbti_3='xxxxo',
            user_mbti_4='xxxxo',
            user_school='서울대학교',
            user_kakaoid='tlarbdnjs33',
            want_age_min=20,
            want_age_max=22,
            want_mbti='istj'
        )
        self.user_female_001 = Profile.objects.create(
            user_model=self.user_joy,
            user_sex=False,
            user_name='조이',
            user_age=20,
            user_mbti_1='xxoxx',
            user_mbti_2='xxxox',
            user_mbti_3='xxxxo',
            user_mbti_4='xxxxo',
            user_school='레드벨벳대학교',
            user_kakaoid='joyjoy',
            want_age_min=20,
            want_age_max=22,
            want_mbti='istj'
        )
        self.user_female_002 = Profile.objects.create(
            user_model=self.user_wendy,
            user_sex=False,
            user_name='웬디',
            user_age=20,
            user_mbti_1='oxxxx',
            user_mbti_2='xxxox',
            user_mbti_3='xxxxo',
            user_mbti_4='xxxxo',
            user_school='레드벨벳대학교',
            user_kakaoid='wendy',
            want_age_min=20,
            want_age_max=22,
            want_mbti='enfp'
        )

    def test_matching(self):
        response = self.client.get('/survey/result/')
        soup = BeautifulSoup(response.content, 'html.parser')
        area = soup.find('div')
        self.assertIn(self.user_female_001.user_name, area.text)
        self.assertNotIn(self.user_female_002.user_name, area.text)
