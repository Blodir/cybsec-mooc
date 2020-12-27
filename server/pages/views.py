from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Message
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import sqlite3
import json


@login_required
def addView(request):
	target = User.objects.get(username=request.POST.get('to'))
	Message.objects.create(source=request.user, target=target, content=request.POST.get('content'))
	return redirect('/')

def deleteView(request):
	conn = sqlite3.connect('server/db.sqlite3')
	c = conn.cursor()
	i = request.POST.get('id')

	c.execute('DELETE FROM pages_message WHERE id='+i)
	conn.commit()

	#Message.objects.get(pk=request.POST.get('id')).delete()
	return redirect('/')

@login_required
def homePageView(request):
	messages = Message.objects.filter(Q(source=request.user) | Q(target=request.user))
	users = User.objects.exclude(pk=request.user.id)
	return render(request, 'pages/index.html', {'msgs': messages, 'users': users})
