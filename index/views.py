from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def main(request):
	return render(request, 'mainpage.html',)

def login(request):
	return render(request,'signup.html',)

