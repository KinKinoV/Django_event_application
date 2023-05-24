from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from .forms import RegisterUserForm,EditSettingsForm,PasswordChangingForm, UserProfileForm,UserProfilePageForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView,CreateView
from django.db.models import Q

from Diploma_website.basic_auth import BasicAuthenticationDefender



class CreateProfilePageView(CreateView):
    model=UserProfile
    form_class=UserProfilePageForm
    template_name="pages/create_user_profile_page.html"
    #fields='__all__'
    
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    

class ShowProfilePageView(DetailView):
    model = UserProfile
    template_name = 'pages/user_profile.html'
    pass

    def get_context_data(self,*args,**kwargs):
        users = UserProfile.objects.all()
        context = super(ShowProfilePageView,self).get_context_data(*args,**kwargs)
        page_user=get_object_or_404(UserProfile, id=self.kwargs['pk'])
        context['page_user']=page_user
        return context

def password_success(request):
    return render(request,'pages/password_success.html')

class PasswordsChangeView(PasswordChangeView):
    form_class=PasswordChangingForm
    #form_class = PasswordChangeForm
    success_url=reverse_lazy('home')

# class UserRegisterView(generic.CreateView):
#     form_class=RegisterUserForm
#     template_name='authenticate/register_user.html'
#     success_url=reverse_lazy('login')
  
#     def get_object(self):
#         return self.request.user
    
class EditProfilePageView(generic.UpdateView):
    model=UserProfile
    template_name='pages/my_profile_edit.html'
    fields=['avatar','bio']
    success_url=reverse_lazy('home')
    
class UserEditView(generic.UpdateView):
    form_class=EditSettingsForm
    template_name='pages/my_settings_edit.html'
    success_url=reverse_lazy('home')
    
    def get_object(self):
        return self.request.user

def register_user(request):
    registred = False
    if request.method=="POST":
        form = RegisterUserForm(request.POST)
        profile=UserProfileForm(request.POST)
        if form.is_valid() and profile.is_valid():
            user = form.save()
            avatar = profile.save(commit=False)
            avatar.user=user
            if 'avatar' in request.FILES:
                avatar.avatar=request.FILES['avatar']
            avatar.save()
            registred = True
            messages.success(request,("Registration were successful"))
            return redirect('home')
    else:
        form = RegisterUserForm()
        profile = UserProfileForm()
    return render(request,'authenticate/register_user.html',{
        'form':form,
        'profile':profile,
        })

def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        BasicAuthenticationDefender(request)
        if user is not None:
            login(request, user)
            return redirect('home')
            # Redirect to a success page.
        else:
            messages.success(request,'There was an error logging in, try again')
            return redirect('login')
                # Return an 'invalid login' error message.
    else:
        return render(request, 'authenticate/login.html')
    
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'You were logged out successfully')
        return redirect('home')
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')


def show_my_page(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        return render(request, 'pages/my_user_profile.html',
                        {
                            'user':user,
                        })
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')

#function to create users profiles pages
def show_page(request,user_id):
    #taking all users content by theirs id created by django itself
    if request.user.is_authenticated:
        user = User.objects.get(pk=user_id)
        return render(request, 'pages/user_profile.html',
                        {
                            'user_id':int(user_id),
                            'user':user,
                        })
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')


def users_profiles(request):
    if request.user.is_authenticated:
        users_profiles=User.objects.all()
        return render(request,'pages/users_profiles.html',
                    {
                        'users_profiles':users_profiles,
                    })
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')

def my_page(request,user_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=user_id)
        return render(request, 'pages/my_profile.html',
                        {
                            'user_id':int(user_id),
                            'user':user,
                        })
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')
    # user_avatar=UserProfile.objects.get(pk=user_id)
    # if user_avatar:
    #     return render(request, 'pages/user_profile.html',
    #                 {
    #                     'user':user,
    #                     'user_avatar':user_avatar,
    #                 })
    # else:
    #     return render(request, 'pages/user_profile.html',
    #                 {
    #                     'user':user,

    #                 })
# Create your views here.

def search_user(request):
    #checking if the request is POST that means the info from searching bar came to our site
    if request.user.is_authenticated:
        if request.method == "POST":

                #taking the valuable by name from POST message  
                searched_user = request.POST['searched_user']
                #filtering the venues by the name from the search field
                users=User.objects.filter(Q(username__contains=searched_user)|Q(first_name__contains=searched_user)|Q(last_name__contains=searched_user))
                return render(request, 'pages/search_user.html',
                        {
                            'searched_user': searched_user, 
                            'users':users,
                        })
        else:
            return render(request, 'pages/search_user.html',
                    {})
    else:
        messages.success(request,('You Aren`t Authorized'))
        return redirect('home')