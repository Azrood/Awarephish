from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    type_question = models.CharField('Type de question', max_length=100)
    question_text = models.TextField(max_length=500)
    difficulty = models.CharField('Difficulté', max_length=10)
    note = models.SmallIntegerField()
    image = models.ImageField(upload_to='questions', null=True)

class Reponses(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answers = models.CharField('Réponses', max_length=100)
    correct_answer = models.CharField('Réponse correct', max_length=100)

class Devoir(models.Model):
    type_devoir = models.CharField("Type de devoir", max_length=100)
    difficulty_devoir = models.CharField("niveau du devoir",max_length=50)
    duree = models.IntegerField("durée estimée")
    contenu = models.FileField(upload_to='devoirs/%Y/%m/%d/',null=True)
    texte = models.TextField("Texte", max_length=500, null=True)

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #usernam, mdp, email
    score_actuel = models.IntegerField()
    niveau_actuel = models.CharField('Niveau', max_length=50)
    homework = models.ManyToManyField(Devoir)

class Quiztest(models.Model): # test in mcd
    difficulty_test = models.CharField("difficulté du test", max_length=50)
    questions = models.ManyToManyField(Question)
    users = models.ManyToManyField(Utilisateur)

class Progres(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_test = models.DateTimeField("Date de test")
    score_test = models.IntegerField()




    
