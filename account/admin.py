from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'status', 'is_admin', 'is_author')
    list_filter = ('is_admin', 'is_author', 'status')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_author', 'status')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Register User', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name',
                       'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username', 'first_name',
                     'last_name',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
