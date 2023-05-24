from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError
from .models import UserProfile
from django.core.files.images import get_image_dimensions

class UserProfilePageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar','bio')
        widgets = {
            'bio':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
        }

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control'}))
    #address=forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email','password1','password2',)
    
    def checking_usernames(self):
        username=self.cleaned_data.get('username')
        user_qs=User.objects.filter(username=username)
        if user_qs.exists():
            raise forms.ValidationError('Username already used')
        return username
    
    def checking_emails(self):
        email=self.cleaned_data.get('email')
        user_qs=User.objects.filter(email=email)
        if user_qs.exists():
            raise forms.ValidationError('Email already used')
        return email
    
    def __init__(self,*args,**kwargs):
        super(RegisterUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'
 #       self.fields['userprofile.avatar'].widget.attrs['class']='form-control'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        form_class=RegisterUserForm
        fields=('bio','avatar')
        
class EditSettingsForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control'}))
    #address=forms.CharField(max_length=100)
    is_active=forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    last_login=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    date_joined=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

    
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email','password','last_login','date_joined','is_active')

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1 = forms.CharField(max_length=40,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 = forms.CharField(max_length=40,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    #address=forms.CharField(max_length=100)
    

    
    class Meta:
        model = User
        fields = ('old_password', 'new_password1','new_password2')

# class UserProfileForm(forms.ModelForm):
    
#     class Meta:
#         model = UserProfile
    
#     def clean_avatar(self):
#         avatar = self.cleaned_data['avatar']
        
#         return avatar