from django.db import models

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



# 어드민 모델 등록 
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # score = models.FloatField(default=0) 
    # json_field = models.JSONField(default=dict)
    def __str__(self):
        return f'제목: {self.question_text}, 날짜: {self.pub_date}'
        
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

# 예전으로 돌아가기 위해 # python manage.py migrate polls 0001 