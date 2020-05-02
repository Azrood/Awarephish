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
]