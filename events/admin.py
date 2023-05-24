from django.contrib import admin
from .models import Venue
from .models import Event, Comment
from django.contrib.auth.models import User, Group
#adding models into admin zone

#admin.site.register(User)
#admin.site.register(Event)
#admin.site.unregister(Group)
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    #add info about venues
    list_display = ('name', 'address', 'phone')
    #add ordering by name in alphabetic order
    ordering = ('name',)
    #fields which we can look for
    search_fields=('name','address')
#admin.site.register(Venue,VenueAdmin)

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name','venue'),'event_date','description','manager','attendees' ,'approved')
    list_display = ('name','event_date','venue')
    list_filter=('event_date','venue')
    ordering=('event_date',) 
    
admin.site.register(Comment)