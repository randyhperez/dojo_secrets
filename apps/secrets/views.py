# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Users, Secrets, Likes

# Create your views here.
def index(request):
    return render(request, 'secrets/index.html')

def log_reg(request):
    if request.method == 'POST':
        if request.POST['action'] == 'register':
            response = Users.objects.validate(request.POST)
        elif request.POST['action'] == 'login':
            response = Users.objects.login(request.POST)
        if not response[0]:
            for error in response[1]:
                messages.error(request, error)
        else:
            request.session['id'] = response[1].id
            request.session['fName'] = response[1].fName
            return redirect('secrets')
    return redirect('/')


def secrets(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'secrets': Secrets.objects.get_secrets(),
        'likes': Likes.objects.get_likes(),
        'user_likes': Secrets.objects.test(request.session['id'])
    }
    testing = Secrets.objects.test(request.session['id'])
    print 'session id', request.session['id']
    for test in testing:
        print 'secret id', test.id, 'user id', test.users.id, test.users.fName, test.id
    if request.session['id'] in testing:
        print 'YOLOLOLOLOL'
    return render(request, 'secrets/secrets.html', context)

def post(request):
    if request.method == 'POST':
        Secrets.objects.post_secret(request.POST['secret'], request.session['id'])
    return redirect('secrets')


def likes(request, secret_id):
    Likes.objects.like_secret(request.session['id'], secret_id)
    return redirect('secrets')

def delete(request, secret_id):
    if request.method == 'POST':
        Secrets.objects.filter(id=secret_id).delete()
    return redirect('secrets')

def popular(request):
    if 'id' not in request.session:
        return redirect('index')
    context = {
        'secrets': Secrets.objects.popular_secrets()
    }
    return render(request, 'secrets/popular.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')
