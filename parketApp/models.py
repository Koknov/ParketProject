from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        if password is None:
            raise TypeError('Users must have a password.')
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return "{} [{}]".format(self.username, self.password)


class Location(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    address = models.CharField(max_length=255)


class ProductGroup(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    group = models.CharField(max_length=255)


class Controller(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    led_controller = models.CharField(max_length=255)


class ItemType(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    type_item = models.CharField(max_length=255)


class Status(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    status = models.CharField(max_length=255)


class Stand(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    location_id = models.ForeignKey(Location, to_field='id', on_delete=models.RESTRICT)
    status_id = models.ForeignKey(Status, to_field='id', on_delete=models.RESTRICT)
    time = models.DateTimeField(auto_now_add=True)
    group_id = models.ForeignKey(ProductGroup, to_field='id', on_delete=models.RESTRICT)
    etalon_sort = models.SmallIntegerField()
    name = models.CharField(max_length=50)
    about = models.TextField(default=None)


class Section(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    stand_id = models.ForeignKey(Stand, to_field='id', on_delete=models.RESTRICT)
    time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    size = models.SmallIntegerField()
    led_controller_id = models.ForeignKey(Controller, to_field='id', on_delete=models.RESTRICT)
    led_pin_prefix = models.CharField(max_length=10)
    is_etalon = models.BooleanField(default=False)


class Item(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    section_id = models.ForeignKey(Section, to_field='id', on_delete=models.RESTRICT)
    type_id = models.ForeignKey(ItemType, to_field='id', on_delete=models.RESTRICT)
    time = models.DateTimeField(auto_now_add=True)
    place = models.SmallIntegerField()
    page_id = models.SmallIntegerField()
    price = models.IntegerField()
    comment = models.CharField(max_length=255)
    status_id = models.ForeignKey(Status, to_field='id', on_delete=models.RESTRICT)
    led_number = models.SmallIntegerField()
