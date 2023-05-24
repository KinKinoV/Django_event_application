from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import UserProfile

class ProfileInLine(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInLine]

admin.site.register(UserProfile)
# Register your models here.
# admin.site.unregister(User)
# admin.site.register(User,UserAdmin)
