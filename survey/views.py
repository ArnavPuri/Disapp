from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 
from survey.models import Question, Survey, Response, AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple, AndroidResponse, UserResponse, UserQuestionResponse
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
	# requestbody = 
	#  '[{"How many mosquitos have you noticed (seen or heard) during the last two days while you were at home?":"Very few (1-2)","Have you seen mosquitoes with white stripes on it\'s body and legs during the last two days while you were at home?":"No","Approximately how many mosquito bites have you received in the last two days while you were at home?":"Some (3-10)","Including you, how many members of your family while staying at home with you have gotten dengue in the last one year?":"2","Have you heard of any cases of dengue in your neighborhood in the last one month, including cases in local hospitals?":"Some (3-10)"},{"latitude":19.1068386,"longitude":72.898207,"useremail":"arnav@teachcoder.in","contact":"8879046058"}]''
	# body.decode('utf-8')
	
	if request.method == 'POST':
		body_unicode = request.body
		body = json.loads(body_unicode)
	# body = request.body
	# body_unicode = requestbody.decode('utf-8')
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




