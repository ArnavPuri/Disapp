# DST backend code

Technologies used
- Python 
- Django Web Framework

## How to setup the code in your machine?
- Download the zip or clone the project in your computer. 
- Install virtualenv and start virtual env
- Inside virtual env run 
<code> pip install -r requirements.txt </code>

- Then run 
<code> python manage.py makemigrations </code>
and 
<code> python manage.py migrate </code>

## Files of interest
### views.py
- JSON parsing and storing of the survey responses from the Android is being handled in <code>def AndroidSubmit</code> method
- User feedback from android app is being handled in <code>def submit_feedback</code> method

### urls.py
- Views (logic) is bind with the urls here

### models.py
- All the structures are defined here 
***Survey Model***
This consist of a name and description field and this model act as a foreign key for other models like,  questions and responses.

***Question model***
Multiple question types are defined in this model. We can have text question, integer question etc.

***User Response and User Question Response***
These models are used to handle the response from Android users
	

