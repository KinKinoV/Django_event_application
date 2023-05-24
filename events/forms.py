from django import forms
from django.forms import ModelForm
from .models import Venue,Event, Comment
from django.contrib.auth.models import User

#creating forms based on imported models
#Admin SuperUser Form
class EventFormAdmin (ModelForm):
    class Meta:
        model=Event
        fields=['q']
        fields = ('name','event_date','venue','manager','description','attendees')
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'manager': 'Manager',
            'description': '',
            'attendees': 'Attendees',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'Event Date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'Venue'}),
            'manager':forms.Select(attrs={'class':'form-select','placeholder':'Manager'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Attendees'}),
        }

#User Event Form
class EventForm(ModelForm):
    class Meta:
        model=Event
        fields = ('name','event_date','venue','description','attendees')
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'description': '',
            'attendees': 'Attendees',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'Event Date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'Venue'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Attendees'}),
        }

#create a venue form
class VenueForm(ModelForm):
    class Meta:
        model=Venue
        fields = ('name','address','zip_code','phone','web_address','email_address','venue_image')
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web_address': '',
            'email_address': '',
            'venue_image':'',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Name'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Zip-code'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone number'}),
            'web_address':forms.TextInput(attrs={'class':'form-control','placeholder':'Web address'}),
            'email_address':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email address'}),
        }

class EditComment(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ('content',)
        widgets = {
        'content':forms.Textarea(attrs={'class':'form-control','placeholder':'comment'}),
        }
        
