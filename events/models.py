from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core import validators

#creating model for venues|locations
#python manage.py makemigrations
#python manage.py migrate
#python manage.py runserver 0.0.0.0:8000
class Venue(models.Model):
    name=models.CharField('Vanue Name', max_length=120)
    address=models.CharField('Vanue address', max_length=300)
    zip_code=models.CharField('Vanue zip code',validators=[validators.validate_integer], max_length=30)
    phone=models.CharField('Contact phone',validators=[validators.validate_integer], max_length=20, blank = True)
    web_address = models.URLField('Website address',max_length=100, blank = True)
    email_address = models.EmailField('Email address',validators=[validators.validate_email], max_length=120, blank = True)
    owner=models.IntegerField('Venue Owner',blank=False, default=1)
    venue_image = models.ImageField(validators=[validators.validate_image_file_extension],null=True,blank=True,upload_to='images/')
    
    def __str__(self):
        return self.name
#model for creating users
# class Regular_Users(models.Model):
#     first_name=models.CharField(max_length=60)
#     last_name=models.CharField(max_length=60)
#     user_email=models.EmailField('User email address')
    
#     def __str__(self):
#         return self.first_name+' '+self.last_name

# Create your models here.
class Event(models.Model):
    name = models.CharField('Event name', max_length=120)
    event_date = models.DateTimeField('Event date', max_length=60)
    venue=models.ForeignKey(Venue,blank = True, null = True, on_delete=models.CASCADE)
    #venue = models.CharField(max_length=120)
    manager = models.ForeignKey(User,blank=True,null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, max_length = 240)
    attendees=models.ManyToManyField(User,related_name='attendees', blank = True)
    approved = models.BooleanField('Approved',default=False)
    def __str__(self):
        return self.name
    
    @property
    def Days_till(self):
        today = date.today()
        days_till=self.event_date.date() - today
        if self.event_date.date()>today:
            days_till_stripped=str(days_till).split(',',1)[0]
        else:
            days_till_stripped=str('Event expired')
        return days_till_stripped
    @property
    def number_of_comments(self):
        return Comment.objects.filter(event=self).count()

class Comment(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   date = models.DateTimeField(auto_now_add=True,)
   event=models.ForeignKey(Event, related_name='comments',on_delete=models.CASCADE)
   content=models.TextField(max_length = 240)
   
   def __str__(self):
       return '%s - %s' % (self.event.name, self.user) 

    