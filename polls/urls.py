from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('some_url', views.some_url), # / 잘 체킹 할것!
    # 아래 변수에서 숫자를 받을 경우, <int:question_id> 으로 표현하고 
    # views 에서 해당 detail 메소드가 있어야함! 그리고 받은 변수가 해당 메소드에 전달 되어야함!
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),  
]
