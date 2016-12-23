from django.contrib import admin
from survey.models import Question, Survey, Response, AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple, AndroidResponse, UserResponse, UserQuestionResponse
# Register your models here.


class QuestionInline(admin.TabularInline):
	model = Question
	extra = 0



class SurveyAdmin(admin.ModelAdmin):
	inlines = [QuestionInline]

class AnswerBaseInline(admin.StackedInline):
	fields = ('question', 'body')
	readonly_fields = ('question',)
	extra = 0

class AnswerTextInline(AnswerBaseInline):
	model= AnswerText  

class AnswerRadioInline(AnswerBaseInline):
	model= AnswerRadio 

class AnswerSelectInline(AnswerBaseInline):
	model= AnswerSelect 

class AnswerSelectMultipleInline(AnswerBaseInline):
	model= AnswerSelectMultiple

class AnswerIntegerInline(AnswerBaseInline):
	model= AnswerInteger 

class ResponseAdmin(admin.ModelAdmin):
	list_display = ('created',) 
	inlines = [AnswerTextInline, AnswerRadioInline, AnswerSelectInline, AnswerSelectMultipleInline, AnswerIntegerInline]
	# specifies the order as well as which fields to act on 
	readonly_fields = ('survey', 'created', 'updated', 'latitude', 'longitude')

class UserAnswerInline(admin.StackedInline):
	fields = ('question', 'response')
	readonly_fields = ('question',)
	extra = 0
	model = UserQuestionResponse

class AndroidResponseAdmin(admin.ModelAdmin):
	list_display = ('created',)
	inlines = [UserAnswerInline]
	readonly_fields = ('created', 'updated', 'latitude', 'longitude')


# admin.site.register(Question, QuestionInline)
# admin.site.register(Category, CategoryInline)
admin.site.register(Survey, SurveyAdmin)

# admin.site.register(Response, ResponseAdmin)

admin.site.register(UserResponse, AndroidResponseAdmin)
# admin.site.register(AndroidResponse)