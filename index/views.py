from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def main(request):
	return render(request, 'mainpage.html',)

@login_required(login_url='/login/')
def storyline(request):
	return render(request,'story.html')

@login_required(login_url='/login/')
def instructions(request):
	return render(request,'instructions.html.html')
	
def login(request):
	return render(request,'main.html',)

