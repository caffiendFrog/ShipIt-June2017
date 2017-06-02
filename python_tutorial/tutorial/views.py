# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from tutorial.authhelper import get_signin_url
from tutorial.outlookservice import get_me
from tutorial.authhelper import get_signin_url, get_token_from_code, get_access_token
from tutorial.outlookservice import get_me, get_my_messages, get_my_events
from datetime import datetime
import time

# Create your views here.

def home(request):
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)
  refresh_token = token['refresh_token']
  expires_in = token['expires_in']

  # expires_in is in seconds
  # Get current timestamp (seconds since Unix Epoch) and
  # add expires_in to get expiration time
  # Subtract 5 minutes to allow for clock differences
  expiration = int(time.time()) + expires_in - 300

  # Save the token in the session
  request.session['access_token'] = access_token
  request.session['refresh_token'] = refresh_token
  request.session['token_expires'] = expiration
  request.session['user_email'] = user['mail']
  return HttpResponseRedirect(reverse('tutorial:mail'))

def mail(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  user_email = request.session['user_email']
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    messages = get_my_messages(access_token, user_email)
    context = { 'messages': messages['value'] }
    return render(request, 'tutorial/mail.html', context)

def events(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  user_email = request.session['user_email']
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    events = get_my_events(access_token, user_email)
    filtered = []
    busyTime = 0;
    for e in events['value']:
      status = e['showAs']
      if (e['isAllDay'] and (status == "busy")) or (status == "busy") or (status == "oof"):
        filtered.append(e)
        startTimeStr = e['start']['dateTime']
        endTimeStr = e['end']['dateTime']
        startTime = datetime.strptime(startTimeStr[0:len(startTimeStr)-1], '%Y-%m-%dT%H:%M:%S.%f')
        endTime = datetime.strptime(endTimeStr[0:len(endTimeStr)-1], '%Y-%m-%dT%H:%M:%S.%f')
        e['delta'] = endTime - startTime
        busyTime = busyTime + (e['delta'].total_seconds()/3600)
# context = { 'events': events['value'] }
    freeTime = (7*5) - busyTime
    context = {'events': filtered, 'busyTime': busyTime, 'freeTime': freeTime}
    return render(request, 'tutorial/events.html', context)
