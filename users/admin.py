from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import Profile, Category


# Register your models here.


# @admin.register(Profile)
# class UserAdmin(ModelAdmin):
#     list_display = ('id', 'email')


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    fields = ('name',)


class ProfileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.is_staff = True
            obj.save()


admin.site.register(Profile, ProfileAdmin)
