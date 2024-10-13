# from django.contrib import admin
# from .models import Question, Choice

# #Register your models here
# # admin.site.register(Question)

# #admin 커트터 마이징하기, 
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('질문 섹션', {'fields': ['question_text']}),
#         ('생성일', {'fields': ['pub_date']}),        
#     ]
#     # readonly_fields = ['pub_date']
#     # inlines = [ChoiceInline]

# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
from django.contrib import admin
from .models import Question, Choice

#ChoiceInline 과 / QuestAdmin으로도 choice 관리 가능해져서 제거  
# admin.site.register(Choice)

# 배치 바꿀 수 있음 
#admin.StackedInline -> 아래로 옵션들을 보여주는거
#admin.TabularInline -> 가로로 배치하여 보여주는 거 
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        # 한글이면 노출이 안됨... ㅎㄷㄷ 영어로 바꾸니까 됨 
        ('Question', {'fields': ['question_text']}),
        ('CreateDate', {'fields': ['pub_date'], 'classes': ['collapse']}),  
    ]
    list_display=('question_text', 'pub_date', 'was_published_recently')
    readonly_fields = ['pub_date']
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    # 질문 text와 choice text를 포함해서 검색 할 수 있음 
    search_fields = ['question_text', 'choice__choice_text']


admin.site.register(Question, QuestionAdmin)
