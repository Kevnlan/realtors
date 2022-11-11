from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Building, Location, Property, Room, Users, Roles, RolePermissions, Permissions


# Register your models here.


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'user_name', 'first_name', 'last_name', 'phone',)
    ordering = ('email',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff',)
    list_filter = ('email', 'user_name', 'phone', 'is_active', 'is_staff',)

    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'phone',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',)}),
        # ('Personal', {'fields': ('first_name', 'last_name', 'phone',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'phone',  'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


# admin.site.register(UserType)
admin.site.register(Users, UserAdminConfig)
admin.site.register(Roles)
admin.site.register(RolePermissions)
admin.site.register(Permissions)
admin.site.register(Property)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Location)
