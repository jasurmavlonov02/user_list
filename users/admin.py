from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import Profile, Category


# Register your models here.


@admin.register(Profile)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'email')


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    fields = ('name',)
