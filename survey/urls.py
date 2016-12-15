from django.conf.urls import url

from . import views

urlpatterns =[
	url(r'^$', views.index, name='index'),
	url(r'^(?P<id>\d+)/$', views.SurveyDetail, name='survey_detail'),
	url(r'^api/$', views.survey_list),
	url(r'^api/(?P<pk>[0-9]+)/$', views.survey_detail)
]