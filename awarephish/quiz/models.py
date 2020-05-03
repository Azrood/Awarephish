from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    type_question = models.CharField('Type de question', max_length=100)
    question_text = models.TextField(max_length=500)
    difficulty = models.CharField('Difficulté', max_length=10)
    note = models.SmallIntegerField()
    image = models.ImageField(upload_to='questions', null=True, blank=True)

    def __str__(self):
        return self.question_text

class Reponses(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    wrong_answers = models.CharField('Réponses Incorrectes', max_length=100, null=True)
    correct_answer = models.CharField('Réponses correctes', max_length=100, null=True)

class Devoir(models.Model):
    type_devoir = models.CharField("Type de devoir", max_length=100)
    difficulty_devoir = models.CharField("niveau du devoir",max_length=50)
    duree = models.IntegerField("durée estimée (min)")
    contenu = models.FileField(upload_to='devoirs/%Y/%m/%d/',null=True,blank=True)
    texte = models.TextField("Texte", max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Devoir {self.difficulty_devoir} : type {self.type_devoir}"


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    score_actuel = models.IntegerField(default=0)
    niveau_actuel = models.CharField('Niveau', max_length=50, default='Débutant')
    homework = models.ManyToManyField(Devoir,blank=True)
    total_reponse = models.IntegerField("nombre total de reponse", default=0)
    total_reponse_correctes = models.IntegerField("nombre de total de reponse correcte", default=0)
    def __str__(self):
        return str(self.user)

class Quiztest(models.Model): # test in mcd
    difficulty_test = models.CharField("difficulté du test", max_length=50)
    questions = models.ManyToManyField(Question)
    users = models.ManyToManyField(Utilisateur)

class Progres(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_test = models.DateTimeField("Date de test")
    score_test = models.IntegerField()




    
