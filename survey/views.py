from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 
from survey.models import Question, Survey, Response, AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple, AndroidResponse, UserResponse, UserFeedback, UserQuestionResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from survey.forms import ResponseForm
from survey.serializers import SurveySerializer, ResponseSerializer
import json

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
    	content = JSONRenderer().render(data)
    	kwargs['content_type'] = 'application/json'
    	super(JSONResponse, self).__init__(content, **kwargs)

def index(request):
	return render(request, 'survey/index.html', {})



def SurveyDetail(request, id):
	survey = Survey.objects.get(id=id)

	if request.method == 'POST':
		form = ResponseForm(request.POST, survey=survey)
		if form.is_valid():
			response = form.save()
			return HttpResponseRedirect("/survey/confirm/")
	else:
		form = ResponseForm(survey=survey)
		#print form
	return render(request, 'survey/survey.html', {'response_form': form, 'survey': survey})


def Confirm(request):
	# email = settings.support_email
	return render(request, 'survey/confirm.html', {})

	def privacy(request):
		return render(request, 'privacy.html')

@csrf_exempt
def AndroidSubmit(request):
	if request.method == 'POST':
		AndroidResponse.objects.create(response_text=request.body)
		return HttpResponse("OK", content_type='json')
	else:
		return HttpResponse("Not Ok", content_type='json')
	return HttpResponse("Not OK", content_type='json')


@csrf_exempt
def AndroidSubmitV2(request):
	if request.method == 'POST':
		body_unicode = request.body
		body = json.loads(body_unicode)
		userContact = body[1]['contact']
		userEmail = body[1]['useremail']
		userLatitude = body[1]['latitude']
		userLongitude = body[1]['longitude']
		submitResponse = UserResponse.objects.create(userEmail=userEmail, userContact=userContact, latitude=userLatitude, longitude=userLongitude)
		questions = body[0]
		for question, response in questions.items():
			UserQuestionResponse.objects.create(question=question, response=response, response_of=submitResponse)
		return HttpResponse("OK", content_type='json')
	else:
		return HttpResponse("Not Ok", content_type='json')
	return HttpResponse("not ok", content_type='json')



@csrf_exempt
def survey_list(request):
	if request.method == 'GET':
		surveys = Survey.objects.all()
		serializer = SurveySerializer(surveys, many=True)
		return JSONResponse(serializer.data)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SurveySerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
			return JSONResponse(serializer.errors, status=400)


@csrf_exempt 
def survey_detail(request, pk):
	try:
		survey = Survey.objects.get(pk=pk)
	except Survey.DoesNotExist:
		return HttpResponse(status=404)

		if request.method=="GET":
			serializer = SurveySerializer(survey)
			return JSONResponse(serializer.data)

		elif request.method == 'DELETE':
			survey.delete()
			return HttpResponse(status=204)



@csrf_exempt
def response_list(request):
	if request.method == 'GET':
		response = Response.objects.all()
		serializer = ResponseSerializer(response, many=True)
		return JSONResponse(serializer.data)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = ResponseSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
			return JSONResponse(serializer.errors, status=400)



@csrf_exempt 
def response_detail(request, pk):
	try:
		response = Response.objects.get(pk=pk)
	except Response.DoesNotExist:
		return HttpResponse(status=404)

		if request.method=="GET":
			serializer = ResponseSerializer(response)
			return JSONResponse(serializer.data)
		elif request.method == 'DELETE':
			response.delete()
			return HttpResponse(status=204)



@csrf_exempt
def submit_feedback(request):
	if request.method == 'POST':
		body_unicode = request.body
		body = json.loads(body_unicode)
		userContact = body['contact']
		userEmail = body['useremail']
		userRating = body['rating']
		feedback = body['feedback']
		UserFeedback.objects.create(userEmail=userEmail, userContact=userContact, rating=userRating, feedback=feedback)
		return HttpResponse("OK", content_type='json')
	else:
		return HttpResponse("Not Ok", content_type='json')
	return HttpResponse("not ok", content_type='json')