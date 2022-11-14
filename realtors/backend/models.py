from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify 

import environ

env = environ.Env()
environ.Env.read_env()


class CustomAccountManager(BaseUserManager):
    def create_superuser(self,email,  user_name, first_name, last_name, phone, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email=email, user_name=user_name, first_name=first_name, last_name=last_name,
                                     phone=phone, password=password, **other_fields)

    def create_user(self, email, user_name, first_name, last_name, phone, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, last_name=last_name, phone=phone,
                          **other_fields)
        user.set_password(password)
        user.save()

        return user


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(_('email address'), max_length=50, unique=True)
    phone = models.CharField(_('phone number'), max_length=50, unique=True)
    status = models.CharField(max_length=50)
    role_id = models.ForeignKey("Roles", on_delete=models.CASCADE, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name', 'phone']

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user_name


class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class RolePermissions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    role_id = models.ForeignKey("Roles", on_delete=models.CASCADE, null=True)
    permission_id = models.ForeignKey("Permissions", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Permissions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    action = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    no_of_buildings = models.IntegerField(default=1)
    property_type = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,blank=True, null=True)
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Property, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return env('local_host_link') + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return env('local_host_link') + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return env('local_host_link') + self.thumbnail.url
            else:
                return ''

    @staticmethod
    def make_thumbnail(image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Building(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    no_of_units = models.IntegerField()
    rent = models.IntegerField()
    amenities = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True, null=True)
    property_id = models.ForeignKey("Property", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + str(self.property_id))
        super(Building, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return env('local_host_link') + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return env('local_host_link') + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return env('local_host_link') + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    room_size = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,blank=True, null=True)
    building_id = models.ForeignKey("Building", on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.id) + str(self.building_id))
        super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return env('local_host_link') + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return env('local_host_link') + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return env('local_host_link') + self.thumbnail.url
            else:
                return ''

    @staticmethod
    def make_thumbnail(image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    plus_codes = models.CharField(max_length=20)
    slug = models.SlugField(unique=True,blank=True, null=True)
    property_id = models.ForeignKey("Property", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.id )+ self.location_name)
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return self.location_name
