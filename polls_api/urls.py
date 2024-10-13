from django.urls import path
from .views import *
# from . import views

urlpatterns = [
    # path('question/', views.question_list, name='question_list'),
    # path('question/<int:id>/', views.question_detail, name='question-detail'),
    path('question/', QuestionList.as_view(), name='question_list'),
    path('question/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),    
]