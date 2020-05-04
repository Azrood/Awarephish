import random
import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import SignupForm, SigninForm
from .models import Utilisateur, Question, Progres, Quiztest
from .utils import evaluate_level, get_user_answers
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
            print(dir(form))
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
    return render(request,'quiz/account.html')

def level_quiz(request):
    r = set(Question.objects.all())
    #TODO : replace 2 with appropriate (and take from each 'niveau')
    phishset = random.sample(r,2)
    quiz = {question : {reponse : reponse.correct_answer for reponse in question.reponses_set.all()} for question in phishset}
    return render(request,'quiz/level-quiz.html',{'quiz':quiz})

def result(request):
    #TODO : return proper result
    user_answers = get_user_answers(request)
    question_ids=[ int(x) for x in request.POST.get('id').split(",")[:-1] ]
    score=0
    scoretest=0
    for questid in question_ids:
        question = get_object_or_404(Question, pk=questid)
        answer_score = question.note / question.reponses_set.filter(correct_answer__isnull=False).count()
        scoretest+= question.note
        for answer in user_answers:
            if question.reponses_set.filter(Q(wrong_answers=answer) | Q(correct_answer=answer)):
                if question.reponses_set.filter(correct_answer=answer):
                    score += answer_score
    score = round(score/scoretest,2)*10
    level = evaluate_level(score)
    return JsonResponse({'status':1,'result':"<p>bravo votre resultat est 5 vous avez un niveau NUL</p>"})

@login_required(login_url='/signin/')
def phishquiz(request):
    user = get_object_or_404(Utilisateur, user=request.user)
    quiz = random.choice(Quiztest.objects.filter(difficulty_test=user.niveau_actuel))
    return render(request,'quiz/phishing-quiz.html',{'quiz':quiz})

def resultquiz(request):
    # TODO: return proper result
    user = get_object_or_404(Utilisateur, user=request.user)

    questions = get_object_or_404(Quiztest, pk=int(request.POST.get('id'))).questions.all()
    user_answers = get_user_answers(request)
    score = 0
    scoretest = 0
    for question in questions:
        answer_score = question.note / question.reponses_set.filter(correct_answer__isnull=False).count()
        scoretest+= question.note
        for answer in user_answers:
            if question.reponses_set.filter(Q(wrong_answers=answer) | Q(correct_answer=answer)):
                if question.reponses_set.filter(correct_answer=answer):
                    score += answer_score

    score = round(score/scoretest,2)*10
    level = evaluate_level(score)
    return JsonResponse({'status':1})

    
#TODO : HOW TO GIVE HOMEWORK ????
@login_required
def progress(request):
    return NotImplemented