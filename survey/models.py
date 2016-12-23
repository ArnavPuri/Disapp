from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class Survey(models.Model):
	"""survey class (wrapper of questions)"""
	name = models.CharField(max_length=40)
	description = models.TextField()

	def questions(self):
		if self.pk:
			return Question.objects.filter(survey=self.pk)
		else:
			return None

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name


def validate_list(value):
	'''takes a text value and verifies that there is at least one comma '''
	values = value.split(',')
	if len(values) < 2:
		raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")


class Question(models.Model):
	"""question model"""
	TEXT = 'text'
	RADIO = 'radio'
	SELECT = 'select'
	SELECT_MULTIPLE = 'select-multiple'
	INTEGER = 'integer'

	QUESTION_TYPES = (
		(TEXT, 'text'),
		(RADIO, 'radio'),
		(SELECT, 'select'),
		(SELECT_MULTIPLE, 'Select Multiple'),
		(INTEGER, 'integer'),
	)

	text = models.TextField()
	required = models.BooleanField()
	survey = models.ForeignKey(Survey)
	question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)

	choices = models.TextField(blank=True, null=True,
		help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')

	def save(self, *args, **kwargs):
		if (self.question_type == Question.RADIO or self.question_type == Question.SELECT 
			or self.question_type == Question.SELECT_MULTIPLE):
			validate_list(self.choices)
		super(Question, self).save(*args, **kwargs)

	def get_choices(self):
		''' parse the choices field and return a tuple formatted appropriately
		for the 'choices' argument of a form widget.'''
		choices = self.choices.split(',')
		choices_list = []
		for c in choices:
			c = c.strip()
			choices_list.append((c,c))
		choices_tuple = tuple(choices_list)
		return choices_tuple

	def __unicode__(self):
		return (self.text)
	
	def __str__(self):
		return self.text


class Response(models.Model):
	# a response object is just a collection of questions and answers with a
	# unique interview uuid
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	survey = models.ForeignKey(Survey)
	conditions = models.TextField('Conditions during interview', blank=True, null=True)
	latitude = models.DecimalField('Latitude', max_digits=11, decimal_places=8, blank=True, null=True)
	longitude = models.DecimalField('Longitude', max_digits=11, decimal_places=8, blank=True, null=True)

	def __unicode__(self):
		return (self.survey.name)
		



class AnswerBase(models.Model):
	question = models.ForeignKey(Question)
	response = models.ForeignKey(Response)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


class AnswerText(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerRadio(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelect(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelectMultiple(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerInteger(AnswerBase):
	body = models.IntegerField(blank=True, null=True)

class AndroidResponse(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	response_text = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return (self.response_text)

	def __str__(self):
		return self.response_text



class UserResponse(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	# survey = models.ForeignKey(Survey)
	userEmail = models.CharField(max_length=255)
	userContact = models.CharField(max_length=255)
	latitude = models.DecimalField('Latitude', max_digits=12, decimal_places=8, blank=True, null=True)
	longitude = models.DecimalField('Longitude', max_digits=12, decimal_places=8, blank=True, null=True)
	
	def __unicode__(self):
		return (self.userEmail)

	def __str__(self):
		return self.userEmail

class UserQuestionResponse(models.Model):
	question = models.TextField(blank=True, null=True)
	response = models.TextField(blank=True, null=True) 
	response_of = models.ForeignKey(UserResponse)


class UserFeedback(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	userEmail = models.CharField(max_length=255)
	userContact = models.CharField(max_length=255)
	rating = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
	feedback = models.TextField(blank=True, null=True)