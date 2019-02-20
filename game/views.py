from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Game,PlayerUser,Board
from random import randint
import logging
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
###for get_current_users()
from django.contrib.auth.models import User
import requests
from django.contrib import auth
from django.contrib.auth.models import User
import json

usr = get_user_model()
print("yayyy")
print(usr.score)
logger = logging.getLogger('GAME')
UP=0
DOWN=1
LEFT=2
RIGHT=3
@ensure_csrf_cookie
def index(request):
	print("calling index")
	
	game = Game()

	games = Game.objects.all()

	return render(request, 'db.html', {'games': games})

def do(request):
	print("calling do")
	if request.method == 'GET':    # page is called by 'get' request
		print("get")
		return create()
	
	elif request.method == 'POST': #directions are taken by 'post' request
		print("post")
		logger.info(request.body)
		print("request")
		print(request.body)   		

		data = json.loads(request.body)  # parsing json string {'data','direction'}    ***here face choosen is req from frontend
		print(data)      # {"board":[0,0,2,0,0,0,0,0,0,0,0,0,0,2,0,0],"direction":0}     

		return process(data)
	
	return create()

def process(data):
	print("calling process")
	# oasis = 0, apogee = 1, blah blah = 2,blah blah = 3, blah blah = 4, blah blah = 5, blah blah = 6
	# current_player = Player.objects.get(name = user)
	board = data['board']
	direction = data['direction']
	#current_player_face_selected  = data['face_selected']  ***from frontend
	#if current_player_face_selected=='oasis':
	#	current_player.face = 0


	#Collapse by direction
	#collapse(board,direction,current_player, current_player_face_selected)

	collapse(board,direction)
	#Add new element
	lose = addNew(board)
	#Build response
	response = {}
	response['board'] = board
	response['continue'] = (lose==False)
	# response['score'] = current_player.score
	print("response : ",response)    # response :  {'board': [0, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'continue': True}
	logger.info(response)
	return JsonResponse(response,safe=False)    # *** to frontend

#def collapse(board,direction,current_player):
def collapse(board,direction):
	print("calling collapse")
	collapsed = False
	for i,e in enumerate(board):
		print(board)
		print(i)
		j = nextIndex(i,direction)  # i is index in nextIndex(index,direction)
		print("j value")
		print(j)
		print(board[i])
		#print(board[j])
		if j>=0 and j <=15:
			if board[i] == board[j] and board[i] != 0:
				
				logger.info("Collapsing %d,%d in %d and %d" % (board[i],board[j],i,j))
				#collapseResult(board,i,j,current_player)
				collapseResult(board,i,j)
				collapsed= True
			if board[j] != 0 and board[i] == 0:
				
				logger.info("Collapsing zeros %d,%d in %d and %d" % (board[i],board[j],i,j))
				collapseZeroResult(board,i,j)
				collapsed= True
	if collapsed == True:
		collapse(board,direction)

#def collapseResult(board,i,j,current_player):
def collapseResult(board,i,j):
	print("calling collapseResult")
	board[i] = board[i]*2;
	board[j] = 0
	print("summmmm")
	print(board[i] + board[i])
	#current_player.score + = board[i]
	#current_player.save()

#def collapseZeroResult(board,i,j,current_player):  # it just shifts blocks up or down or left or right
def collapseZeroResult(board,i,j):
	print("calling collapseZeroResult")
	board[i] = board[j];
	board[j] = 0

#Position board
# 00 01 02 03
# 04 05 06 07
# 08 09 10 11
# 12 13 14 15
def nextIndex(index,direction):
	print("calling nextIndex")

	if direction == UP:
		return index +4;
	elif direction == DOWN:
		return index -4
	elif direction == LEFT:
		if (index+1) % 4 ==0:
			return -1
		return index+1
	elif direction == RIGHT:
		if index  % 4 ==0:
			return -1
		return index-1

def addNew(board):
	#Search free spots
	print("calling addNew")
	free = []
	for i,e in enumerate(board):
		print(i,e)
		if e==0:
			free.append(i)
	#Asign 2 to a random free spots
	if len(free) >0 :
		i = randint(0,len(free)-1)
		print("Next spot index %d of %d"% (i,len(free)))
		print("Next spot in %d" % (free[i]))
		board[free[i]] = 2
		return False
	else:
		return True
	
def create():
	print("calling create")
	#Create a new board with random 2 spots
	data =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	first = randint(0,15)
	second = randint(0,15)
	while first == second:
		second = randint(0,15)
	data[first] = 2;
	data[second] = 2;
	#data[player] = user;   ***if req by frontend
	print("wohooo")
	return JsonResponse(data,safe=False)    



def checkAnswer(request):
    #if not request.user.is_authenticated() :
    #   return redirect('/main/login')
    #if(timer(request)<0):
    #   logout(request)
    #   return redirect('/')
    
    if request.method == 'POST':
        #if(timer(request)<0):
            #return JsonResponse
        dt = json.loads(request.body.decode('utf-8'))
        answer = dt['answer']
        qsno=request.user.currentQs
        qs=Question.objects.get(questionno=qsno)
        #print(answer)
    
        if qs.solution==answer:
            request.user.score+=50
            user.currentQs +=1;
            # print("s")
            print(qs.solution)
            request.user.save()
            #return redirect("mainpage/")
            return JsonResponse({'user':request.user.name, 'score':request.user.score})
    
        request.user.save()
        #return redirect("mainpage/")
        return JsonResponse({'user':request.user.name, 'score':request.user.score})

    else:
        return HttpResponse("yayyy")