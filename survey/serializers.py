from rest_framework import serializers
from survey.models import Survey, Response, Question


class ResponseSerializer(serializers.ModelSerializer):
	# questions = serializers.StringRelatedField(many=True)
	class Meta:
		model = Response
		fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model= Question
		fields='__all__'
			
class SurveySerializer(serializers.ModelSerializer):
	questions = QuestionSerializer(many=True)
	class Meta:
		model = Survey
		fields = '__all__'
