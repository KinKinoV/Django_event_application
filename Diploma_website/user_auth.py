import base64
import binascii

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from rest_framework import serializers, exceptions, HTTP_HEADER_ENCODING
from rest_framework.exceptions import ValidationError
from defender import utils as defender_utils
from defender import config
from rest_framework.authentication import (
    get_authorization_header,
)

# Get the UserModel
UserModel = get_user_model()

class BasicAuthenticationDefender(serializers.Serializer):

   username = serializers.CharField(required=False, allow_blank=True)
   email = serializers.EmailField(required=False, allow_blank=True)
   password = serializers.CharField(style={'input_type': 'password'})

   def authenticate(self, **kwargs):
     request = self.context['request']

     if hasattr(settings, 'ACCOUNT_AUTHENTICATION_METHOD'):
         login_field = settings.ACCOUNT_AUTHENTICATION_METHOD
     else:
         login_field = 'username'
     userid = self.username_from_request(request, login_field)

     if defender_utils.is_already_locked(request, username=userid):
         detail = "You have attempted to login {failure_limit} times with no success. ".format(
                      failure_limit=config.FAILURE_LIMIT,
                      cooloff_time_seconds=config.LOCKOUT_COOLOFF_TIME[defender_utils.get_lockout_cooloff_time(username=userid)]
                  )
         raise exceptions.AuthenticationFailed(_(detail))

     login_unsuccessful = False
     login_exception = None
     try:
         response = authenticate(request, **kwargs)
         if response == None:
             login_unsuccessful = True
             msg = _('Unable to log in with provided credentials.')
             # raise exceptions.ValidationError(msg)
             login_exception = exceptions.ValidationError(msg)
     except exceptions.AuthenticationFailed as e:
         login_unsuccessful = True
         login_exception = e

     defender_utils.add_login_attempt_to_db(request,
                                            login_valid=not login_unsuccessful,
                                            username=userid)

     user_not_blocked = defender_utils.check_request(request,
                                                     login_unsuccessful=login_unsuccessful,
                                                     username=userid)
     if user_not_blocked and not login_unsuccessful:
         return response

     raise login_exception

   def _validate_email(self, email, password):
     user = None

     if email and password:
         user = self.authenticate(email=email, password=password)
     else:
         msg = _('Must include "email" and "password".')
         raise exceptions.ValidationError(msg)

     return user

   def _validate_username(self, username, password):
     user = None

     if username and password:
         user = self.authenticate(username=username, password=password)
     else:
         msg = _('Must include "username" and "password".')
         raise exceptions.ValidationError(msg)

     return user

   def _validate_username_email(self, username, email, password):
     user = None

     if email and password:
         user = self.authenticate(email=email, password=password)
     elif username and password:
         user = self.authenticate(username=username, password=password)
     else:
         msg = _('Must include either "username" or "email" and "password".')
         raise exceptions.ValidationError(msg)

     return user

   def validate(self, attrs):
     username = attrs.get('username')
     email = attrs.get('email')
     password = attrs.get('password')

     user = None

     if 'allauth' in settings.INSTALLED_APPS:
         from allauth.account import app_settings

         # Authentication through email
         if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
             user = self._validate_email(email, password)

         # Authentication through username
         elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
             user = self._validate_username(username, password)

         # Authentication through either username or email
         else:
             user = self._validate_username_email(username, email, password)

     else:
         # Authentication without using allauth
         if email:
             try:
                 username = UserModel.objects.get(
                     email__iexact=email).username()
             except UserModel.DoesNotExist:
                 pass

         if username:
             user = self._validate_username_email(username, '', password)

     # Did we get back an active user?
     if user:
         if not user.is_active:
             msg = _('User account is disabled.')
             raise exceptions.ValidationError(msg)
     else:
         msg = _('Unable to log in with provided credentials.')
         raise exceptions.ValidationError(msg)

     # If required, is the email verified?
     if 'rest_auth.registration' in settings.INSTALLED_APPS:
         from allauth.account import app_settings
         if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
             email_address = user.emailaddress_set.get(email=user.email)
             if not email_address.verified:
                 raise serializers.ValidationError(
                     _('E-mail is not verified.'))

     attrs['user'] = user
     return attrs

   def username_from_request(self, request, login_field):
     user_data = request._data
     return user_data[login_field]