from django.conf.urls import url

from . import views

urlpatterns =[
	url(r'^$', views.index, name='index'),
	url(r'^(?P<id>\d+)/$', views.SurveyDetail, name='survey_detail'),
	url(r'^api/survey$', views.survey_list),
	url(r'^api/survey/(?P<pk>[0-9]+)/$', views.survey_detail),
	url(r'^confirm/$', views.Confirm),
	url(r'^api/response/$', views.response_list),
	url(r'^api/response/(?P<pk>[0-9]+)/$', views.response_detail),
	url(r'^androidresponse$', views.AndroidSubmit),
	url(r'^androidresponseV2$', views.AndroidSubmitV2),
	url(r'^androidfeedback$', views.submit_feedback),

]