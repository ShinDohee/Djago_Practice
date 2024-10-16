from polls.models import Question, Choice, Vote
from polls_api.serilaizers import QuestionSerializer, UserSerializer, RegisterSerializer, VoteSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly, IsVoter
from rest_framework import status
from rest_framework.response import Response

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status , mixins
# from django.shortcuts import render , get_object_or_404
# # Create your views here.
# from rest_framework.views import APIView

# 메소드를 선언해서, http 메소드에 따라 분기하여 구현함 
# @api_view(['GET', 'POST'])
# def question_list(request):    
#     if request.method == 'GET':
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many = True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             #에러일 시 나오는 응답 처리 
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
# @api_view(['GET', 'PUT', 'DELETE'])
# def question_detail(request, id):
#     question = get_object_or_404(Question, pk=id)
    
#     if request.method == 'GET':
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:    
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class기반 구현 방법 
# class QuestionList(APIView):
#     def get(self, request):
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class QuestionDetail(APIView):
#     def get(self, request, id):
#         question = get_object_or_404(Question, pk=id)
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)

#     def put(self, request, id):
#         question = get_object_or_404(Question, pk=id)
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:    
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, id):
#         question = get_object_or_404(Question, pk=id)
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    



# class기반 구현 방법 
#Mixin 으로 만든 코드 
# class QuestionList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
# # APIVIEW대신 mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView 를 매개변수로 받으면
# # 공통 적으로 호출하는 질문리스트 받아오는거나, serializer하는 부분 전역변수로 뺄 수 있음 
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     #대신 매게변수에 *argm, **kwargs 추가 
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# class QuestionDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
        
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class기반 구현 Generic으로 만든 
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        #원래 owner는 readonly 라서 값을 설정 못하지만
        #save 할때는 주어지는 변수들을 사용하기 때문에 owner를 지정하여 저장할 수 있다 
        serializer.save(owner=self.request.user)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer    

class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter=self.request.user)
    #Mixin 함수를 오버라이드 함 
    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data['voter'] = request.user.id
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsVoter]
    
    def perform_update(self, serializer):
        serializer.save(voter=self.request.user)
