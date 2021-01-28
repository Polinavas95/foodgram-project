from django.contrib import admin, auth

from .models import User


class Admin(auth.admin.UserAdmin):
    '''
    Expand functionality in admin site.
    '''
    list_filter = ('username', 'email', )
    search_fields = ('^username', '^email', )
    ordering = ('username', )


admin.site.register(User, Admin)
