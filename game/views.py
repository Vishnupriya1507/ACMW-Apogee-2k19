from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Game
from random import randint
import logging
import json

logger = logging.getLogger('GAME')
UP=0
DOWN=1
LEFT=2
RIGHT=3;
@ensure_csrf_cookie
def index(request):

    game = Game()

    games = Game.objects.all()
    print(games)
    print(type(games))

    return render(request, 'db.html', {'game': games})
    #return HttpResponse("hellooo")

def do(request):
	if request.method == 'GET':
		return create()
	elif request.method == 'POST':
		logger.info(request.body)
		data =json.loads(request.body)
		return process(data)
	return create()

def process(data):
	board = data['board']
	direction = data['direction']
	#Collapse by direction
	collapse(board,direction)
	#Add new element
	lose = addNew(board)
	#Build response
	response = {}
	response['board'] = board
	response['continue'] = (lose==False)
	logger.info(response)
	return JsonResponse(response,safe=False)	

def collapse(board,direction):
	collapsed = False
	for i,e in enumerate(board):
		j = nextIndex(i,direction)
		if j>=0 and j <=15:
			if board[i] == board[j] and board[i] != 0:
				logger.info("Collapsing %d,%d in %d and %d" % (board[i],board[j],i,j))
				collapseResult(board,i,j)
				collapsed= True
			if board[j] != 0 and board[i] == 0:
				logger.info("Collapsing zeros %d,%d in %d and %d" % (board[i],board[j],i,j))
				collapseZeroResult(board,i,j)
				collapsed= True
	if collapsed == True:
		collapse(board,direction)

def collapseResult(board,i,j):
	board[i] = board[i]*2;
	board[j] = 0

def collapseZeroResult(board,i,j):
	board[i] = board[j];
	board[j] = 0

#Position board
# 00 01 02 03
# 04 05 06 07
# 08 09 10 11
# 12 13 14 15
def nextIndex(index,direction):

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
	free = []
	for i,e in enumerate(board):
		if e==0:
			free.append(i)
	#Asign 2 to a random free spots
	if len(free) >0 :
		i = randint(0,len(free)-1)
		logger.info("Next spot index %d of %d"% (i,len(free)))
		logger.info("Next spot in %d" % (free[i]))
		board[free[i]] = 2
		return False
	else:
		return True
	
def create():
	#Create a new board with random 2 spots
	data =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	first = randint(0,15)
	second = randint(0,15)
	while first == second:
		second = randint(0,15)
	data[first] = 2;
	data[second] = 2;
	return JsonResponse(data,safe=False) 