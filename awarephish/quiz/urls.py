from django.urls import path

from . import views

urlpatterns = [
    path('',views.redir, name='redir'),
    path('index/', views.index,name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('conseils/', views.conseils, name='conseils'),
    path('account/', views.account, name="account"),
    path('level-quiz/', views.level_quiz, name="level-quiz"),
    path('result/', views.result, name="result"),
    path('phishquiz/', views.phishquiz, name="phishquiz"),
    path('account/progres', views.progress, name="progress"),
    path('resultquiz/', views.resultquiz, name="resultquiz"),
    path('account/homework/', views.homework, name='homework'),
    path('accout/viewprogres/', views.view_progress, name='view-progress'),
]