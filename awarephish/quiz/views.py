import random
import datetime

from statistics import mean

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone

from .forms import SignupForm, SigninForm
from .models import Utilisateur, Question, Progres, Quiztest, Devoir
from .utils import evaluate_level, get_user_answers, message_level, get_nextlevel_score
# Create your views here.

def redir(request):
    return redirect('/index/')

def index(request):
    return render(request,"quiz/index.html")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            Utilisateur(user=user, score_actuel=0).save()
            login(request, user)
            return redirect('/index/')
    else:
        form = SignupForm()
    return render(request,'quiz/signup.html/',{'form':form})

def signin(request):
    if request.method == 'POST':
        form = SigninForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                    username= form.cleaned_data['username'],
                    password=form.cleaned_data['password'])
            login(request, user)
            return redirect('/index/')
    else:
        form = SigninForm()
    return render(request, 'quiz/signin.html',{'form':form})


@login_required
def signout(request):
    logout(request)
    return redirect('/index/')

def conseils(request):
    return render(request,'quiz/conseil.html')

def account(request):
    user = get_object_or_404(Utilisateur, user=request.user)
    return render(request,'quiz/account.html',{'score':user.score_actuel,
                                                'users':user,
                                                'next':get_nextlevel_score(user.niveau_actuel),
                                                'progress':round((user.score_actuel/get_nextlevel_score(user.niveau_actuel))*100,2),
                                                'remainder':get_nextlevel_score(user.niveau_actuel) - user.score_actuel,
                                                'ratio':round((user.total_reponse_correctes/user.total_reponse)*100,2),
                                                'mean': mean(p.score_test for p in user.progres_set.all())
                                                })

def level_quiz(request):
    r=[]
    for level in ["Niveau 1","Niveau 2", "Niveau 3"]:
        r += random.sample(
                set(Question.objects.filter(difficulty=level)),
                2)
    phishset = r.copy()
    quiz = {question : {reponse : reponse.correct_answer for reponse in question.reponses_set.all()} for question in phishset}
    return render(request,'quiz/level-quiz.html',{'quiz':quiz})

def result(request):
    user_answers = get_user_answers(request)
    question_ids=[int(x) for x in request.POST.get('id').split(",")[:-1] ]
    score=0
    scoretest=0
    for questid in question_ids:
        question = get_object_or_404(Question, pk=questid)
        answer_score = question.note / question.reponses_set.filter(correct_answer__isnull=False).count()
        scoretest += question.note
        user_answers_copy = user_answers.copy()

        for answer in user_answers_copy:
            if question.reponses_set.filter(Q(wrong_answers=answer) | Q(correct_answer=answer)):
                user_answers.remove(answer)
                if question.reponses_set.filter(correct_answer=answer):
                    score += answer_score
                else:
                    score -= answer_score

    score = max(round(score/scoretest,2)*300, 0)
    level = evaluate_level(score)
    message = message_level(level)
    return JsonResponse({'status':1,'score':score, 'level':level,'message':message})

@login_required(login_url='/signin/')
def phishquiz(request):
    user = get_object_or_404(Utilisateur, user=request.user)
    quiztest = random.choice(Quiztest.objects.filter(difficulty_test=user.niveau_actuel).exclude(users=user))
    quiztest.users.set([user])
    quiztest.save()
    quiz = {quest : [rep for rep in quest.reponses_set.all()] for quest in quiztest.questions.all()}
    return render(request,'quiz/phishing-quiz.html',{'quiz':quiz, 'quiztest':quiztest})

def resultquiz(request):
    user = get_object_or_404(Utilisateur, user=request.user)

    questions = get_object_or_404(Quiztest, pk=int(request.POST.get('id'))).questions.all()
    user_answers = get_user_answers(request)
    score = 0
    scoretest = 0
    nbr_reponse, nbr_reponse_correcte = 0,0

    for question in questions:
        answer_score = question.note / question.reponses_set.filter(correct_answer__isnull=False).count()
        scoretest += question.note
        user_answers_copy = user_answers.copy()
        for answer in user_answers_copy:
            if question.reponses_set.filter(Q(wrong_answers=answer) | Q(correct_answer=answer)):
                user_answers.remove(answer)
                if question.reponses_set.filter(correct_answer=answer):
                    score += answer_score
                    nbr_reponse_correcte += 1
                    nbr_reponse += 1
                else:
                    nbr_reponse += 1
                    score -= answer_score
    coef = get_nextlevel_score(user.niveau_actuel)
    
    score = max(round(score,2), 0)
    user.score_actuel = min(round(user.score_actuel + score, 2),300)
    user.total_reponse += nbr_reponse
    user.total_reponse_correctes += nbr_reponse_correcte

    user.niveau_actuel = evaluate_level(user.score_actuel)
    try:
        homeworks = [random.choice(Devoir.objects.filter(difficulty_devoir=user.niveau_actuel,type_devoir=typ).exclude(utilisateur=user))for typ in ["video","texte"]]
    except IndexError:
        homeworks=[]

    user.homework.set(homeworks+list(user.homework.all()))
    
    user.progres_set.create(date_test=timezone.now(), score_test=score)
    user.save()
    next_level = get_nextlevel_score(user.niveau_actuel)

    return JsonResponse({'status':1, 'result':score,'actual':user.score_actuel , 'level':user.niveau_actuel,'next':next_level})

    


def view_progress(request):
    user = get_object_or_404(Utilisateur, user=request.user)
    prog = { 
            'x':[p.date_test for p in user.progres_set.all()],
            'y': [p.score_test for p in user.progres_set.all()],
    }
    return JsonResponse({'status':1, 'progress':prog})

@login_required
def homework(request):
    user = get_object_or_404(Utilisateur, user=request.user)
    devoirs = user.homework.all()
    return render(request,'quiz/homework.html',{'devoir':devoirs})

@login_required
def progress(request):
    return render(request,"quiz/progress.html")