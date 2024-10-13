#테스트를 위한 import
from django.test import TestCase
from polls.models import Question, Choice, Vote
from polls_api.serilaizers import QuestionSerializer, VoteSerializer
from django.contrib.auth.models import User 
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

class QuestionListTest(APITestCase):
    def setUp(self):
        self.question_data = {'question_text': 'some question'}
        self.url = reverse('question_list')


    def test_create_question(self):
        user =User.objects.create(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.question_text, self.question_data['question_text'])
        self.assertLess((timezone.now() - question.pub_date).total_seconds(), 1)


    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_list_question(self):
        question = Question.objects.create(question_text='Question1')
        choice = Choice.objects.create(question=question, choice_text='Choice1')
        Question.objects.create(question_text='Question2')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['choices'][0]['choice_text'], choice.choice_text)




class QuestionSerializerTestCase(TestCase):
    def test_with_valid_data(self):
        serializer = QuestionSerializer(data={'question_text': 'abc'})
        self.assertEqual(serializer.is_valid(), True)
        new_question = serializer.save()
        self.assertIsNotNone(new_question.id)
        
    def test_with_invalid_data(self):
        serializer = QuestionSerializer(data={'question_text': ''})
        self.assertEqual(serializer.is_valid(), False)

    # 테스트 메소드 실행을 위해선 test_ 로 메소드 명이 시작해야함 

class VoteSerializerTest(TestCase):
    # 테스트 할때마다 실행 하는 메소드 
    #각 테스트 별 공통으로 쓰는 코드들은 여기다가 
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.question = Question.objects.create(
            question_text='abc',
            owner=self.user,
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text='1'
        )    

    def test_vote_serializer(self):  
        self.assertEqual(User.objects.all().count(), 1)
        data = {
            'question': self.question.id,
            'choice': self.choice.id,
            'voter': self.user.id,
        }
        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        vote = serializer.save()
    
        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self.user)
    
    def test_vote_serializer_with_duplicate_vote(self):
        self.assertEqual(User.objects.all().count, 1)
        choice1 = Choice.objects.create(
            quetsion=self.question,
            choice_text='2'
        )
        Vote.objects.create(question=self.question, choice=self.choice, voter=self.user)
    
        data = {
            'question': self.question.id,
            'choice': self.choice.id,
            'voter': self.user.id,
        }
        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_vote_serilaizer_with_unmatched_question_and_choice(self):
        question2 = Question.objects.create(
            question_text='abc',
            owner=self.user,
        )
    
        choice2 = Choice.objects.create(
            quetsion=question2,
            choice_text='1'
        )
        data = {
            'question': self.question.id,
            'choice': choice2.id,
            'voter': self.user.id,
        }
        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
