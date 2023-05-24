from django.urls import path
from . import views
from .views import EditProfilePageView,UserEditView,PasswordsChangeView,ShowProfilePageView,CreateProfilePageView#,UserRegisterView,
from django.contrib.auth import views as auth_views
from Diploma_website.user_auth import BasicAuthenticationDefender

urlpatterns = [
   #path('login_user',views.login_user, name='login'),
   #path('logout_user',views.logout_user, name='logout'),
   #path('register_user',UserRegisterView.as_view(), name='register_user'),
   path('register_user',views.register_user, name='register_user'),
   path('<user_id>/show_page/',views.show_page, name='show-page'),
   path('users_profiles',views.users_profiles, name='users-profiles'),
   path('my_settings_edit/', UserEditView.as_view(), name='my-settings-edit'),
   #path('password/', auth_views.PasswordChangeView.as_view(template_name='pages/change-password.html'), name='my-profile-edit'),
   path('password/', PasswordsChangeView.as_view(template_name='pages/change-password.html'), name='password-change'),
   path('password_success/', views.password_success, name='password-success'),
   #path('<int:pk>/profile/',ShowProfilePageView.as_view(), name='profile-view'),
   path('<int:pk>/my_profile_edit/', EditProfilePageView.as_view(), name='my-profile-edit'),
   path('create_profile_page/', CreateProfilePageView.as_view(), name='create-profile-page'),
   path('show_my_page/', views.show_my_page, name='show-my-page'),
   path('shearch_user/', views.search_user, name='search-user'),
  # path('logusr',BasicAuthenticationDefender,name='usrlog'),
]