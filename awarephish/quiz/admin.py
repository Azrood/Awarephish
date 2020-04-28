from django.contrib import admin
from .models import Question, Quiztest, Reponses, Devoir, Utilisateur

# Register your models here.
class ReponsesAdmin(admin.TabularInline):
    model = Reponses
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets =[
        (None,  
            {'fields': ['type_question',('difficulty','note')]}),

        ("Contenu", 
            {
                'fields':['question_text','image']}),
    ]
    inlines = [ReponsesAdmin]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiztest)
admin.site.register(Utilisateur)
admin.site.register(Devoir)