from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect


def main(request):
	return render(request, 'mainpage.html',)