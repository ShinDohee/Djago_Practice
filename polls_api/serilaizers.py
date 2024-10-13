from rest_framework import serializers
from polls.models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueTogetherValidator

# #ModelSerializer로 만들면, create, update 정의안해줘도 자동으로 만들어짐!
# class QuestionSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')

#     class Meta:
#         model = Question
#         fields = ['id', 'question_text', 'pub_date', 'owner']
# class QuestionSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     question_text = serializers.CharField(max_length=200)
#     #pubdate 자동생성이니까 read_only 를 trun라고함
#     pub_date = serializers.DateTimeField(read_only=True)

#     # json 에 저장할땐 유효성을 통과한 데이터로 저장 해야함 ! 그래서 validated_data
#     def create(self, validated_data):
#         return Question.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.question_text = validated_data.get('question_text', instance.question_text) + '[시리얼 라이즈에서 업데이트]'
#         instance.save()
#         return instance

# class UserSerializer(serializers.ModelSerializer):
#     #user 와 quesetion의 1:다 의 관계를 표현 
#     questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'questions']
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "두 패스워드가 일치하지 않습니다."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()        
        return user
    
    class Meta:
        model = User
        fields = ['username', 'password','password2']

class ChoiceSerializer(serializers.ModelSerializer): 
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['choice_text', 'votes_count']
    
    def get_votes_count(self, obj):
        return obj.vote_set.count()
    
class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'owner', 'choices']

class UserSerializer(serializers.ModelSerializer):
    #questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    #유저읭 Question 이 보여지는 
    # questions = serializers.StringRelatedField(many=True, read_only=True)
    #특정 필드를 지정할 수 있는 (pub_date를 지정)
    # questions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pub_date')
    # url 로 절달하는 
    questions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='question-detail')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'questions']


class VoteSerializer(serializers.ModelSerializer):    
    def validate(self, attrs):
        if attrs['choice'].question.id != attrs['question'].id:
            raise serializers.ValidationError("Question과 Choice가 조합이 맞지 않습니다.")
        
        return attrs
        
    class Meta:
        model = Vote
        fields = ['id', 'question', 'choice', 'voter']
        validators = [
            UniqueTogetherValidator(
                queryset=Vote.objects.all(),
                fields=['question', 'voter']
            )
        ]