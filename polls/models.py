from django.db import models

from django.utils import timezone
import datetime
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.
# dB를 테이블별로 읽어서, 도와주는 파일 

# 모델 생성 
# class Question, class Choice(models.Model) 함수 작성

#모델을 테이블에 써주기 위한 마이그레이션 
# settings.py의 INSTALLED_APPS에  'polls.apps.PollsConfig', 을 추가 
#그리고 터미널에서 
# python manage.py makemigrations polls  // 마이그레이션 파일 생성


# 모델에 맞는 테이블 생성
#  python manage.py migrate             //마이그레이션 실행 

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#     # is_something = models.BooleanField(default=False)
#     # average_score = models.FloatField(default=0.0)

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

# 모델에서 수정을 하면 무조건 shell 에서 migration 을 해줘야함 


# 어드민 모델 등록 
class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='질문')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
# on_delete=models.CASCADE옵션은 owner가 삭제되면 Question 도 지우라는 뜻
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE, null=True)
    # score = models.FloatField(default=0) 
    # json_field = models.JSONField(default=dict)
    @admin.display(boolean=True, description='최근생성(하루기준)')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def __str__(self):
        # if self.was_published_recently():
        #     new_badge = 'NEW!!!'
        # else:
        #     new_badge = ''
        return f'제목: {self.question_text}, 날짜: {self.pub_date}'
        
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'voter'], name='unique_voter_for_questions')
        ]
# 예전으로 돌아가기 위해 # python manage.py migrate polls 0001