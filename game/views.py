
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Game,PlayerUser,Board ,Question
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
from datetime import timedelta, datetime
from django.utils import timezone

import json


usr = get_user_model()
print("yayyy")
#print(request.user)
logger = logging.getLogger('GAME')
UP=0
DOWN=1
LEFT=2
RIGHT=3
# @ensure_csrf_cookie



#@login_required(login_url='/login/')
def timer(user_):
    # if request.user.is_authenticated():
    #print("yayyy")
    user_.time =float(200-(timezone.now()-user_.regTime).total_seconds())
    #print("yoyoyo")
    # print(timezone.now())
    # print(user_.regTime)
    print((timezone.now()-user_.regTime).total_seconds())
    user_.save()
    # return HttpResponse("yoyaayy")
    return float(user_.time)


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
        if(timer(request.user)<0):
            print("time over")
            return redirect('/login/')
        revealQues(request)
        # checkAnswer(request)
        # print("post")
        # logger.info(request.body)
        print("request")
        # print(request.body)  
        global current_player 
        #current_player = request.user  
        #current_player = PlayerUser.objects.create(name = request.user)  
        # print(request.user.score)   
        # print(request.user)
        data = json.loads(request.body)  # parsing json string {'data','direction'}    ***here face choosen is req from frontend
        print(data)      # {"board":[0,0,2,0,0,0,0,0,0,0,0,0,0,2,0,0],"direction":0}     

        return process(data,request.user)
    
    return create()

def process(data,user_):
    print("calling process")
    # oasis = 0, apogee = 1, blah blah = 2,blah blah = 3, blah blah = 4, blah blah = 5, blah blah = 6
    
    board = data['board']
    direction = data['direction']
    #current_player_face_selected  = data['face_selected']  ***from frontend
    #if current_player_face_selected=='oasis':
    #   current_player.face = 0

    user_score = user_.score
    #Collapse by direction
    #collapse(board,direction,current_player, current_player_face_selected)

    collapse(board,direction,user_)
    #Add new element
    lose = addNew(board)
    #Build response
    response = {}
    response['board'] = board
    response['continue'] = (lose==False)
    response['score'] = user_score
    response['board_state'] = True
    print("response : ",response)    # response :  {'board': [0, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'continue': True}
    logger.info(response)
    return JsonResponse(response,safe=False)    # *** to frontend

#def collapse(board,direction,current_player):
def collapse(board,direction,user_):
    print("calling collapse")
    collapsed = False
    for i,e in enumerate(board):
        # print(board)
        # print(i)
        j = nextIndex(i,direction)  # i is index in nextIndex(index,direction)
        # print("j value")
        # print(j)
        # print(board[i])
        #print(board[j])
        if j>=0 and j <=15:
            if board[i] == board[j] and board[i] != 0:
                
                logger.info("Collapsing %d,%d in %d and %d" % (board[i],board[j],i,j))
                collapseResult(board,i,j,user_)
                #collapseResult(board,i,j)
                collapsed= True
            if board[j] != 0 and board[i] == 0:
                
                logger.info("Collapsing zeros %d,%d in %d and %d" % (board[i],board[j],i,j))
                collapseZeroResult(board,i,j,user_)
                collapsed= True
    if collapsed == True:
        collapse(board,direction,user_)

#def collapseResult(board,i,j,current_player):
def collapseResult(board,i,j,user_):
    print("calling collapseResult")
    board[i] = board[i]*2;
    board[j] = 0
    # print("summmmm")
    #print(board[i] + board[i])
    user_.score = user_.score + board[i]
    user_.save()
    print(user_.score)
    #current_player.score = current_player.score +  board[i]
    #print(current_player.score)
    #current_player.save()

#def collapseZeroResult(board,i,j,current_player):  # it just shifts blocks up or down or left or right
def collapseZeroResult(board,i,j,user_):
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
        # print(i,e)
        if e==0:
            free.append(i)
    #Asign 2 to a random free spots
    if len(free) >0 :
        i = randint(0,len(free)-1)
        # print("Next spot index %d of %d"% (i,len(free)))
        # print("Next spot in %d" % (free[i]))
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
    # print("wohooo")
    return JsonResponse(data,safe=False)    



def revealQues(request):
    # if not request.user.is_authenticated() :
        # return redirect('/main/login')
    
    data = {}
    count = (200-request.user.time)/(request.user.currentQs*20)
    if(count >=1 ):
        curr_ques = Question.objects.get(questionno = request.user.currentQs)
        data['curr_ques_num'] = curr_ques.questionno
        data['curr_ques_Ques'] = curr_ques.question
        #data['curr_ques_ans'] = curr_ques.solution
        data['board_state'] = False
        request.user.currentQs = request.user.currentQs + 1
        request.user.save()
        print(data)
        return JsonResponse(data,safe=False)
        

def checkAnswer(request):
    #if not request.user.is_authenticated() :
    #   return redirect('/main/login')
    if(timer(request.user)<0):
    #   logout(request)
        return redirect('/')
    
    if request.method == 'POST':
        #if(timer(request)<0):
            #return JsonResponse
        dt = json.loads(request.body.decode('utf-8'))
        answer = dt['answer']
        qsno=request.user.currentQs - 1
        qs=Question.objects.get(questionno=qsno)
        #print(answer)
    
        if qs.solution==answer:
            request.user.score+=10000
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