from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 
from survey.models import Question, Survey, Response, AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple
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
from forms import ResponseForm
from survey.serializers import SurveySerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def index(request):
	return HttpResponse("Hello World!")



def SurveyDetail(request, id):
	survey = Survey.objects.get(id=id)

	if request.method == 'POST':
		form = ResponseForm(request.POST, survey=survey)
		if form.is_valid():
			response = form.save()
			return HttpResponseRedirect("/confirm/")
	else:
		form = ResponseForm(survey=survey)
		#print form
	return render(request, 'survey/survey.html', {'response_form': form, 'survey': survey})

def Confirm(request, uuid):
	email = settings.support_email
	return render(request, 'confirm.html', {"email": email})

def privacy(request):
	return render(request, 'privacy.html')





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