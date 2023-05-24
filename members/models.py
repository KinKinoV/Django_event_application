from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",related_name="followed_by",symmetrical=False, blank=True,)
    avatar=models.ImageField(null=True,blank=True,upload_to='images/profile')
    bio = models.TextField(blank=True, max_length = 240)
    
    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse("home")
    

