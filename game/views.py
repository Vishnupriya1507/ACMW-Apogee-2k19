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

import functools
from contextlib import ContextDecorator
from datetime import datetime, timedelta, tzinfo
from threading import local

import pytz

from django.conf import settings


import json

usr = get_user_model()
print("yayyy")
#print(request.user)
logger = logging.getLogger('GAME')
UP=0
DOWN=1
LEFT=2
RIGHT=3
#@ensure_csrf_cookie

def get_default_timezone():
    """
    Return the default time zone as a tzinfo instance.

    This is the time zone defined by settings.TIME_ZONE.
    """
    return pytz.timezone(settings.TIME_ZONE)



# This function exists for consistency with get_current_timezone_name
def get_default_timezone_name():
    """Return the name of the default time zone."""
    return _get_timezone_name(get_default_timezone())

_active = local()


def get_current_timezone():
    """Return the currently active time zone as a tzinfo instance."""
    return getattr(_active, "value", get_default_timezone())



def timer(user_):
   
    user_.time = float(7200-(timezone.now()-user_.regTime).total_seconds())
    current_time =  datetime.now()
    print("yoyoyo")
    print("timezone.now()-user_.regTime : ", (timezone.now()-user_.regTime).total_seconds())
    user_.save()
    return float(user_.time)

@login_required(login_url='/login/')
def Acads(request):
    print("calling index")
    
    game = Game()

    games = Game.objects.all()

    return render(request, 'acads.html', {'games': games})


@login_required(login_url='/login/')
def apogee(request):
    print("calling index")
    
    game = Game()

    games = Game.objects.all()

    return render(request, 'apogee.html', {'games': games})



@login_required(login_url='/login/')
def cda(request):
    print("calling index")
    
    game = Game()

    games = Game.objects.all()

    return render(request, 'cda.html', {'games': games})

@login_required(login_url='/login/')
def placements(request):
    print("calling index")
    
    game = Game()

    games = Game.objects.all()

    return render(request, 'placement.html', {'games': games})

@login_required(login_url='/login/')
def oasis(request):
    print("calling index")
    
    game = Game()

    games = Game.objects.all()

    return render(request, 'oasis.html', {'games': games})


@login_required(login_url='/login/')
def bosm(request):
    print("calling index")
    
    game = Game()

    games = Game.objects.all()

    return render(request, 'bosm.html', {'games': games})

@login_required(login_url='/login/')
def do(request):
    print("calling do")
    if request.method == 'GET':    # page is called by 'get' request
        
        print(request.user)
        #print(request.user.face)
        return create()

    elif request.method == 'POST': #directions are taken by 'post' request
        if(timer(request.user)<0):
            print("Time Over")
            #print(timer(request.user))
            #logout(request)
            return redirect('/')
        #revealQues(request)
        
        #{'answer': ,'userw': ,'board_state':false}
        #{'board': ,'direction'}
        print("post")
        print(request)
        logger.info(request.body)
        print("request")
        print(request.body)  
        global current_player 
        #current_player = request.user  
        #current_player = PlayerUser.objects.create(name = request.user)  
        print(request.user.score)   
        print(request.user)
        data = json.loads(request.body)  # parsing json string {'data','direction'}    ***here face choosen is req from frontend
        print(data)      # {"board":[0,0,2,0,0,0,0,0,0,0,0,0,0,2,0,0],"direction":0, "board_state":True/False}     
        # if(data['board_state']!=False):
        #     return process(data,request.user)
        return process(data,request.user,request)
    return create()

#@login_required(login_url='/login/')
def process(data,user_,request):
    print("calling process")
    # oasis = 0, apogee = 1, blah blah = 2,blah blah = 3, blah blah = 4, blah blah = 5, blah blah = 6

    # dict_ = revealQues(request)
    if  data['board_state']==1:
        board = data['board']
        direction = data['direction']
       

        user_score = user_.score
        print("*************************************************************")
        
        #Build response
        
        response = {}
        count = (7200-request.user.time)/(request.user.currentQs*60)
        
        print("request.user.time : ", request.user.time," ","request.user.currentQs*30 : ", request.user.currentQs*30)
        if(count >=1 and (request.user.currentQs<=9)) :
            print("count is >= 1")
            revealQues_dict = revealQues(request)
            print("revealQues_dict['curr_ques_Ques'] : ", type(revealQues_dict['curr_ques_Ques']))
            response['board_state'] = 2
            response['continue'] = True
            response['curr_ques_Ques'] = str(revealQues_dict['curr_ques_Ques'])
        else:
            print("count is not >=1")
            response['board_state'] = 1
            collapse(board,direction,user_)
            #Add new element
            lose = addNew(board)
            # response['continue'] = (lose==False)
            response['continue'] = True
        response['board'] = board
        response['score'] = user_score
        response['timer_time'] = (7200-request.user.time)



    elif data['board_state'] ==2:
        checkAnswer_dict_ =  checkAnswer(request)
        response = {}
        print("response : ",response)     #response :  {'board': [0, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'continue': True, score : 200}
        logger.info(response)
        response['score'] = checkAnswer_dict_['score']
        response['board_state'] = 1
        response['is_correct'] = checkAnswer_dict_['is_correct']
        response['continue'] = True
        response['timer_time'] = (7200-request.user.time)
        print("CHECKING THE ANS SCORE",response)
        # return JsonResponse(response,safe=False)    # *** to frontend
    
    # else is executed when user clicks at that time when ques needs to be displayed
    # frontend sends {"answer":__ , 'user':__}
    elif data['board_state'] == 3:
        response={}
        response['board_state'] = 3
        response['continue'] = True
        response['timer_time'] = (7200-request.user.time)
        
    return JsonResponse(response,safe=False)
        
#@login_required(login_url='/login/')
def collapse(board,direction,user_):
    print("calling collapse")
    collapsed = False
    for i,e in enumerate(board):
        print(board)
        print(i)
        j = nextIndex(i,direction)  # i is index in nextIndex(index,direction)
        print("j value")
        print(j)
        print(board[i])
        
        if j>=0 and j <=15:
            print(board[j])
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

#@login_required(login_url='/login/')
def collapseResult(board,i,j,user_):
    print("calling collapseResult")
    board[i] = board[i]*2;
    board[j] = 0
    print("summmmm")
    #print(board[i] + board[i])
    user_.score = user_.score + board[i]
    user_.save()

#@login_required(login_url='/login/')
def collapseZeroResult(board,i,j,user_):
    print("calling collapseZeroResult")
    board[i] = board[j];
    board[j] = 0

#Position board
# 00 01 02 03
# 04 05 06 07
# 08 09 10 11
# 12 13 14 15
#@login_required(login_url='/login/')
def nextIndex(index,direction):
    print("calling nextIndex")

    if direction == UP:
        return index +4
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

#@login_required(login_url='/login/')
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
    
#@login_required(login_url='/login/')
def create():
    print("calling create")
    #Create a new board with random 2 spots
    data =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    first = randint(0,15)
    second = randint(0,15)
    while first == second:
        second = randint(0,15)
    data[first] = 2
    data[second] = 2
    #data[player] = user;   ***if req by frontend
    print("wohooo")
    return JsonResponse(data,safe=False)    

@login_required(login_url='/login/')
def revealQues(request):
    
    data = {}
    count = (7200-request.user.time)/(request.user.currentQs*60)
    if(count >=1 ):
    # if (request.user.currentQs*60 < count <(request.user.currentQs+1)*60):
        print("revealQues Questionneeds to be popped up")
        curr_ques = Question.objects.get(questionno = request.user.currentQs)
        data['board_state'] = 2
        data['curr_ques_num'] = curr_ques.questionno
        data['curr_ques_Ques'] = curr_ques.question

        request.user.currentQs = request.user.currentQs + 1
        request.user.save()
        print(data)

        
        return data
        
 
@login_required(login_url='/login/')
def checkAnswer(request):
    #if not request.user.is_authenticated() :
    #   return redirect('/main/login')
    # if(timer(request.user)<0):
    #   logout(request)
        # return redirect('/')
    
    if request.method == 'POST':
        #if(timer(request)<0):
            #return JsonResponse
        dt = json.loads(request.body.decode('utf-8'))
        answer = dt['answer']
        print("FRONTEND KA ANS",answer)
        # response['board_state'] = True
        qsno = request.user.currentQs - 1
        qs=Question.objects.get(questionno=qsno)
        #print(answer)
    
        if qs.solution==answer:

            request.user.score+=10000
            print("CHECKING THE ANS SCORE",request.user.score)
            
            # print("s")
            print(qs.solution)
            request.user.save()
            #return redirect("mainpage/")
            dict_ = {}
            dict_['score'] = request.user.score
            dict_['user'] = request.user.name
            dict_['is_correct'] = True
            print("CHECKING THE ANS SCORE",dict_['score'], "dict_ after user's answer is correct :",dict_)
            return dict_
        # request.user.currentQs =request.user.currentQs + 1;
        request.user.save()
        dict_ = {}
        dict_['score'] = request.user.score
        print("request.user.score in checkAnswer", request.user.score)
        dict_['user'] = request.user.name
        dict_['is_correct'] = False
        print("type(dict_): ",type(dict_))
        return dict_

    else:
        return HttpResponse("yayyy")
