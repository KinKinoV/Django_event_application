from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar, month_name
from datetime import datetime

from django.urls import reverse_lazy
from requests import request
from .models import Event, Venue, Comment
from .forms import VenueForm, EventForm, EventFormAdmin,EditComment
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
#import User Model from django
from django.contrib.auth.models import User

from argparse import Namespace

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#Paginator stuff
from django.core.paginator import Paginator
from django.contrib import messages

from django.db.models import Q
from django.views.generic import DetailView,CreateView

from os import uname
def venue_pdf(request):
#create bytestream buffer
    buf=io.BytesIO()
    #create canvas
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    #create a text object
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont('Helvetica',14)
    
    #add venue info
    venues=Venue.objects.all()
    lines=[]
    for venue in venues :
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.phone)
        lines.append(venue.zip_code)
        lines.append(venue.web_address)
        lines.append(venue.email_address)
        lines.append(' ')
    for line in lines:
        textob.textLine(line)
    #drawing all info into pdf
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    #add lines of text
    return FileResponse(buf,as_attachment=True,filename='venue.pdf')

def venue_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    #Designate the model
    #lines = ['This is line 1\n','This is line 2\n', 'This is line 3\n']
    #create a csv writer
    writer = csv.writer(response)
    #Add column heading to csv
    writer.writerow(['Venue Name','Address','Zip code','Phone number', 'Web address', 'Email address'])
    
    #Write lines to Text file
    venues = Venue.objects.all()
    #loop trough the content in model, all venues
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web_address,venue.email_address])
   
    return response

#Generator of txt files of venue list
def venue_text(request):
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    #Designate the model
    #lines = ['This is line 1\n','This is line 2\n', 'This is line 3\n']
    #Write lines to Text file
    venues = Venue.objects.all()
    #create a blank list
    lines = list()
    #loop trough the content in model, all venues
    for venue in venues:
        lines.append(f'{venue}\n{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web_address}\n{venue.email_address}\n\n\n')
    response.writelines(lines)
    return response

def delete_venue(request,venue_id):
    #take the info from database venue model by id that were sent
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

def delete_event(request,event_id):
    if request.user.is_authenticated:
        #take the info from database event model by id that were sent
        event = Event.objects.get(pk=event_id)
        if request.user==event.manager:#or request.user.is_superuser
            event.delete()
            messages.success(request,('Event was deleted {event}'))
            return redirect('event-list')
        else:
            messages.success(request,('You Aren`t Authorized To Delete This Event '))
            return redirect('event-list')
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')
    

#function for updating current event in my database user will sent request and id of venue to update
def update_event(request,event_id):
    if request.user.is_authenticated:
        #take the info from database event model by id that were sent
        event = Event.objects.get(pk=event_id)
        
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST or None,instance = event)
        else:
        #creating the form, lines on the page to edit info with current info in database
            form = EventForm(request.POST or None,instance = event)
        #checking is our changes is legit, correct fulfilled or not 
        if form.is_valid():
            #saving into database
            form.save()
            #redirecting to other page by url name from urls.py
            return redirect('event-list')
        #rendering request and all the data to the html page with valuables in brackets {}, venue info and the form
        return render(request, 'events/update_event.html',
                    {
                        'event': event,
                        'form':form,
                    })
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')

def add_event(request):
    if request.user.is_authenticated:
        submitted = False
        if request.method == 'POST':
            if request.user.is_superuser :#or user.id == {id num}
                form=EventFormAdmin(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/add_event?submitted=True')
            else:
                form = EventForm(request.POST)
                if form.is_valid():
                    #form.save()
                    event = form.save(commit=False)
                    event.manager = request.user
                    event.save()
                    return HttpResponseRedirect('/add_event?submitted=True')      
        else:
            #Just going to page,not submitting
            if request.user.is_superuser:
                form = EventFormAdmin
            else:
                form = EventForm
            if 'submitted' in request.GET:
                submitted=True
        return render(request,'events/add_event.html',{'form':form, 'submitted':submitted,})
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')

#function for updating current venue in my database user will sent request and id of venue to update
def update_venue(request,venue_id):
    if request.user.is_authenticated:
        #take the info from database venue model by id that were sent
        venue = Venue.objects.get(pk=venue_id)
        #creating the form, lines on the page to edit info with current info in database
        form = VenueForm(request.POST or None, request.FILES or None, instance = venue)
        #checking is our changes is legit, correct fulfilled or not 
        if form.is_valid():
            #saving into database
            form.save()
            #redirecting to other page by url name from urls.py
            return redirect('list-venues')
        #rendering request and all the data to the html page with valuables in brackets {}, venue info and the form
        return render(request, 'events/update_venue.html',
                    {
                        'venue': venue,
                        'form':form,
                    })
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')

def search_venues(request):
    if request.user.is_authenticated:
    #checking if the request is POST that means the info from searching bar came to our site
        if request.method == "POST":
            #taking the valuable by name from POST message  
            searched_venues = request.POST['searched_venues']
            #filtering the venues by the name from the search field
            venues=Venue.objects.filter(name__contains=searched_venues)
            venue=Venue.objects.get(name__contains=searched_venues)
            venue_owner = User.objects.get(pk=venue.owner)
            return render(request, 'events/search_venues.html',
                    {
                        'searched_venues': searched_venues, 
                        'venues':venues,
                        'venue_owner':venue_owner,
                    })
        else:
            return render(request, 'events/search_venues.html',
                    {})
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')
    
    
def show_venue(request,venue_id):
    if request.user.is_authenticated:
        #taking all venues content by theirs id created by django itself
        venue = Venue.objects.get(pk=venue_id)
        venue_owner = User.objects.get(pk=venue.owner)
        #grab events from that venue
        events=venue.event_set.all()
        return render(request, 'events/show_venue.html',
                    {
                        'venue': venue,
                        'venue_owner':venue_owner,
                        'events':events,
                    })
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')

def list_venues(request):
    #taking info about all venues into valuable
    #venue_list = Venue.objects.all().order_by('name')#'?' for random order
    venue_list = Venue.objects.all().order_by('name')
    
    #Set up Paginator
    p= Paginator(Venue.objects.all(), 2)
    page=request.GET.get('page')
    venues=p.get_page(page)
    nums = " " * venues.paginator.num_pages
    
    return render(request, 'events/venues.html',
                  {
                      'venue_list': venue_list,
                      'venues':venues,
                      'nums':nums,
                   })

def all_events(request):
    #taking info about all events into valuable
    eventList = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html',
                  {
                      'eventList':eventList,
                   })

def search_events(request):
    if request.user.is_authenticated:
        #checking if the request is POST that means the info from searching bar came to our site
        if request.method == "POST":
            #taking the valuable by name from POST message  
            searched_events = request.POST['searched_events']
            #filtering the venues by the name from the search field
            events=Event.objects.filter(Q(description__contains=searched_events)|Q(name__contains=searched_events))
            return render(request, 'events/search_events.html',
                    {
                        'searched_events': searched_events, 
                        'events':events,
                    })
        else:
            return render(request, 'events/search_events.html',
                    {})
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')

#show event
def show_event(request,event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(pk=event_id)
        comments=Comment.objects.all()
        return render(request, 'events/show_event.html', {'event':event,'comments':comments,})
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')
    
    # form=EditComment(request.POST or None,initial={'user':request.user,'event':event,})
    # if request=="POST":
    #     if form.is_valid():
    #         form.save()
    #         return redirect('event-list')
    # else:
    #     return render(request, 'events/show_event.html', {'event':event,'form':form,'comments':comments,})

#show events at the venues
def venue_events(request, venue_id):
    #Grab venue info from venues
    venue = Venue.objects.get(id=venue_id)
    #grab events from that venue
    events=venue.event_set.all()
    if events:
        return render(request, 'events/venue_events.html', {'events':events,})
    else:
        messages.success(request,("That venue has no events now"))
        return redirect('admin-approval')

    
#admin event approval page
def admin_approval(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            #get venues
            venue_list=Venue.objects.all
            #get counts
            event_count=Event.objects.all().count()
            venue_count=Venue.objects.all().count()
            user_count=User.objects.all().count()
            event_list=Event.objects.all().order_by('-event_date')
            events_all=Event.objects.all()
            events_all_ids=[]
            for i in range(0,len(events_all),1):
                events_all_ids.append(str(events_all[i].id))
            if request.method=="POST":
                id_list_approve=request.POST.getlist('boxes')
                print(id_list_approve)
                for item in id_list_approve:
                    Event.objects.filter(pk=int(item)).update(approved=True)
                id_set_disaprove = set(events_all_ids)-set(id_list_approve)
                id_list_disaprove=list(id_set_disaprove)
                for y in id_list_disaprove:
                    Event.objects.filter(pk=int(y)).update(approved=False)
                messages.success(request,("Events was/were approved"))
                return redirect('event-list')
            else:
                return render(request,'events/admin_approval.html',
                        {
                            'event_list':event_list,
                            'event_count':event_count,
                            'venue_count':venue_count,
                            'user_count':user_count,
                            'venue_list':venue_list,
                            
                        })
        else:
            messages.success(request,("You are not authorized"))
            return redirect('home')
    else:
        messages.success(request,("You are not authorized"))
        return redirect('home')
    


# My events page
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events=Event.objects.filter(attendees=me)
        return render(request,'events/my_events.html',
                      {
                          'events':events
                      })
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')

def timestuff(year,month):
    #make uppercase for month varuable
    month = month.title()
    #converting month name into num
    month_number = int(list(month_name).index(month))
    #creating html form of calendar
    htmlcal = HTMLCalendar().formatmonth(year, month_number)
    #current date 
    now = datetime.now()
    current_year=now.year
    current_day = now.day
    current_month = now.month
    time = now.strftime('%H:%M:%S')

    
    return ({
        'year':year,
        'month':month,
        'month_number': month_number,
        'htmlcal' : htmlcal,
        'current_year' : current_year,
        'current_day' : current_day,
        'current_month' : current_month,
        'time':time,
        })

def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    vmhost = uname()[1]
    if request.user.is_authenticated:
        username=User.objects.get(pk=request.user.id)
        #Query the Events Model for Dates
        n=Namespace(**timestuff(year,month))
        cur_month=n.month_number
        event_list = Event.objects.filter(attendees=username).filter(event_date__year=year).filter(event_date__month=cur_month)
        return render(request, 'events/home.html',{'time_stuff':timestuff(year,month),'event_list':event_list, 'vmhost':vmhost,})
    else:
        return render(request, 'events/home.html',{'time_stuff':timestuff(year,month),'vmhost':vmhost,})

def Calendar(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    return render (request,'events/calendar.html',timestuff(year,month))

def add_venue(request):
    if request.user.is_authenticated:
        submitted = False
        if request.method == 'POST':
            #using created form VenueForm from file forms.py
            form = VenueForm(request.POST,request.FILES)
            if form.is_valid():
                venue=form.save(commit=False)
                venue.owner = request.user.id #logged in user
                venue.save()
                #form.save()
                return HttpResponseRedirect('/add_venue?submitted=True')
        else:
            form = VenueForm
            if 'submitted' in request.GET:
                submitted=True
        return render(request,'events/add_venue.html',{'form':form, 'submitted':submitted,})
    else:
        messages.success(request,("You are not authorized"))
        return redirect('home')
 
class AddCommentView(CreateView):
    model = Comment
    form_class=EditComment
    template_name="events/add_comment.html"
    success_url=reverse_lazy('event-list',)
    
    def form_valid(self,form):
        form.instance.event_id=self.kwargs['pk']
        form.instance.user_id=self.request.user.id
        return super().form_valid(form)
    
    
