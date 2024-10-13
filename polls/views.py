from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render # 화면에 html 을 그려주는 역할 
# from django.http import Http404
from django.shortcuts import render , get_object_or_404
from django.urls import reverse

# def index(request):
#     return HttpResponse("heelo, wolrld!")

def some_url(request):
    return HttpResponse("some url 구현함")

# order_by(컬럼명)  역순으로 정렬 
# render(request, 'polls/index.html', context) html 에 데이터 그리는 것 
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # 16강 
    # output = '.'.join([q.question_text for q in latest_question_list])   
    # context = {'first_question': latest_question_list[0]}

    #17강
    context = {'questions': latest_question_list}
    #화면에 no Question 확인 용 
    #context = {'questions': []}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    # object가 없으면 404로 처리하라  
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # 아무것도 안누르고 클릭할 경우 방어 처리 
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': '선택이 없습니다.'})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:index'))