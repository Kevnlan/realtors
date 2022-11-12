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


class PropertyConfig(admin.ModelAdmin):
    search_fields = ('name', 'user_id')
    ordering = ('name',)
    list_display = ('name', 'no_of_buildings', 'property_type', 'user_id')
    list_filter = ('name', 'no_of_buildings', 'property_type', 'user_id')

    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Building Details', {'fields': ('no_of_buildings', 'property_type','user_id')}),
        # ('Personal', {'fields': ('first_name', 'last_name', 'phone',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'no_of_buildings', 'property_type', 'user_id')}
         ),
    )


class BuildingConfig(admin.ModelAdmin):
    search_fields = ('property_id', 'image', 'no_of_units', 'rent','amenities')
    ordering = ('id',)
    list_display = ('property_id', 'no_of_units', 'rent', 'amenities','image')
    list_filter = ('property_id', 'no_of_units', 'rent', 'amenities','image')


class RoomConfig(admin.ModelAdmin):
    search_fields = ('building_id', 'user_id')
    ordering = ('id',)
    list_display = ('building_id', 'user_id', 'room_size', 'image')
    list_filter = ('building_id', 'user_id', 'room_size', 'image')


class LocationConfig(admin.ModelAdmin):
    search_fields = ('location_name', 'property_id')
    ordering = ('id',)
    list_display = ('location_name', 'property_id', 'latitude', 'longitude')
    list_filter = ('location_name', 'property_id', 'latitude', 'longitude')


# admin.site.register(UserType)
admin.site.register(Users, UserAdminConfig)
admin.site.register(Roles)
admin.site.register(RolePermissions)
admin.site.register(Permissions)
admin.site.register(Property, PropertyConfig)
admin.site.register(Building, BuildingConfig)
admin.site.register(Room, RoomConfig)
admin.site.register(Location, LocationConfig)
