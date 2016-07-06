# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
    class Meta:
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=30)
    class Meta:
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    class Meta:
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
    class Meta:
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()
    class Meta:
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()
    class Meta:
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'


class Gateway(models.Model):
    id_gateway = models.IntegerField(primary_key=True)
    gateway = models.TextField(blank=True, null=True)  # This field type is a guess.
    class Meta:
        db_table = 'gateway'


class Location(models.Model):
    id_location = models.IntegerField(primary_key=True)
    location = models.TextField(blank=True, null=True)  # This field type is a guess.
    class Meta:
        db_table = 'location'


class Machine(models.Model):
    id_machine = models.IntegerField(primary_key=True)
    cris = models.TextField(blank=True, null=True)  # This field type is a guess.
    memo = models.TextField(blank=True, null=True)  # This field type is a guess.
    system_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    integrated = models.TextField(blank=True, null=True)  # This field type is a guess.
    file_types = models.TextField(blank=True, null=True)  # This field type is a guess.
    ip = models.TextField(blank=True, null=True)  # This field type is a guess.
    ae = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_location = models.ForeignKey(Location, models.DO_NOTHING, db_column='id_location', blank=True, null=True)
    id_manufacturer = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='id_manufacturer', blank=True, null=True)
    id_name_model = models.ForeignKey('NameModel', models.DO_NOTHING, db_column='id_name_model', blank=True, null=True)
    id_gateway = models.ForeignKey(Gateway, models.DO_NOTHING, db_column='id_gateway', blank=True, null=True)
    id_subnet = models.ForeignKey('Subnet', models.DO_NOTHING, db_column='id_subnet', blank=True, null=True)
    id_port = models.ForeignKey('Port', models.DO_NOTHING, db_column='id_port', blank=True, null=True)
    class Meta:
        db_table = 'machine'


class Manufacturer(models.Model):
    id_manufacturer = models.IntegerField(primary_key=True)
    manufacturer = models.TextField(blank=True, null=True)  # This field type is a guess.
    class Meta:
        db_table = 'manufacturer'


class NameModel(models.Model):
    id_name_model = models.IntegerField(primary_key=True)
    name_model = models.TextField(blank=True, null=True)  # This field type is a guess.
    class Meta:
        db_table = 'name_model'


class Port(models.Model):
    id_port = models.IntegerField(primary_key=True)
    port = models.TextField(blank=True, null=True)  # This field type is a guess.
    class Meta:
        db_table = 'port'


class Subnet(models.Model):
    id_subnet = models.IntegerField(primary_key=True)
    subnet = models.TextField(blank=True, null=True)  # This field type is a guess.
    class Meta:
        db_table = 'subnet'
        
