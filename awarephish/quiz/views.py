import random

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, SigninForm
from .models import Utilisateur, Question
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
    r=set(Question.objects.all())
    phishset = random.sample(r,2)
    quiz = {question : {reponse : reponse.correct_answer for reponse in question.reponses_set.all()} for question in phishset}
    return render(request,'quiz/level-quiz.html',{'quiz':quiz})

def result(request):
    user_answers = [k for k,v in request.POST.items() if 'csrfmiddle' not in k][:-1]
    question_ids=[int(x) for x in request.POST.get('id').split(",")[:-1]]
    score=0
    for id in question_ids:
        question=get_object_or_404(Question, pk=id)
        for answer in user_answers:
            if question.reponses_set.filter(answers=answer):
                print(answer)
    return JsonResponse({'status':1,'result':"<p>bravo votre resultat est 5 vous avez un niveau NUL</p>"})



