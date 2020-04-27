from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    type_question = models.CharField('Type de question', max_length=100)
    question_text = models.CharField(max_length=500)
    difficulty = models.CharField('Difficulté', max_length=10)
    note = models.SmallIntegerField()

class Reponses(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answers = models.CharField('Réponses', max_length=100)
    correct_answer = models.CharField('Réponse correct', max_length=100)

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #usernam, mdp, email
    score_actuel = models.IntegerField()
    niveau_actuel = models.CharField('Niveau', max_length=50)
    


class Devoirs(models.Model):
    type_devoir = models.CharField("Type de devoir", max_length=100)
    duree = models.IntegerField()
    difficulty_devoir = models.CharField


class Progres(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_test = models.DateField()
    score_test = models.IntegerField()




    
