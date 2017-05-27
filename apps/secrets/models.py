# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$')

# Create your models here.
class UsersDBManager(models.Manager):
    def validate(self, data):
        errors = []
        unique = Users.objects.filter(email=data['email'])
        if len(data['fName']) < 2:
            errors.append('First name must atleast 2 characters')
        if len(data['lName']) < 2:
            errors.append('Last name must atleast 2 characters')
        if not re.match(NAME_REGEX, data['fName']) or not re.match(NAME_REGEX, data['lName']):
            errors.append('Name fields can only contain letters')
        if not re.match(EMAIL_REGEX, data['email']):
            errors.append('Please enter a valid email address')
        if not re.match(PASSWORD_REGEX, data['psw']) or len(data['psw']) < 8:
            errors.append('Password must be at least 8 characters and contain a lowercase, uppercase, number and symbol ')
        if data['psw'] != data['confpsw']:
            errors.append('Passwords do not match')
        if unique:
            errors.append('Invalid email address please select a different one')
        if errors:
            return [False, errors]
        else:
            psw = data['psw'].encode()
            hash_psw = bcrypt.hashpw(psw, bcrypt.gensalt())
            Users.objects.create(fName=data['fName'], lName=data['lName'], email=data['email'], hash_psw=hash_psw)
            newUser = Users.objects.filter(email=data['email'])
            return [True, newUser[0]]

    def login(self, data):
        errors = []
        verify = Users.objects.filter(email=data['email'])
        psw = data['psw'].encode()
        hash_psw = bcrypt.hashpw(psw, bcrypt.gensalt())
        if not verify:
            errors.append('Invalid email or password')
        elif not bcrypt.checkpw(data['psw'].encode(), verify[0].hash_psw.encode()):
            errors.append('Invalid email or password')
        if errors:
            return [False, errors]
        else:
            return [True, verify[0]]

class SecretsDBManager(models.Manager):
    def post_secret(self, text, id):
        Secrets.objects.create(secret=text, users=Users.objects.get(id=id))
    def popular_secrets(self):
        return Secrets.objects.all().order_by('-secrets_likes')
    def test(self, id):
        return Secrets.objects.filter(secrets_likes__users__id=id)
    def get_secrets(self):
        return Secrets.objects.all().order_by('-created_at')[:10]

class LikesDBManager(models.Manager):
    def like_secret(self, users_id, secrets_id):
        Likes.objects.create(users=Users.objects.get(id=users_id), secrets=Secrets.objects.get(id=secrets_id))
    def get_user_likes(self, id):
        Likes.objects.filter(users__id=id)
    def get_likes(self):
        return Likes.objects.all()

class Users(models.Model):
    fName = models.CharField(max_length=50)
    lName = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    hash_psw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersDBManager()

class Secrets(models.Model):
    secret = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ForeignKey(Users, related_name='users_secrets', on_delete=models.CASCADE)
    objects = SecretsDBManager()

class Likes(models.Model):
    users = models.ForeignKey(Users, related_name='users_likes', on_delete=models.CASCADE)
    secrets = models.ForeignKey(Secrets, related_name='secrets_likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LikesDBManager()
