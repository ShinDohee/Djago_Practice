from django.urls import path, include
from .views import VoteList, VoteDetail, QuestionList, QuestionDetail, UserList, UserDetail, RegisterUser
# from . import views

urlpatterns = [
    # path('question/', views.question_list, name='question_list'),
    # path('question/<int:id>/', views.question_detail, name='question-detail'),
    path('question/', QuestionList.as_view(), name='question_list'),
    path('question/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),  
    path('users/', UserList.as_view(),name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('register/', RegisterUser.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('vote/', VoteList.as_view()),
    path('vote/<int:pk>/', VoteDetail.as_view()),
]