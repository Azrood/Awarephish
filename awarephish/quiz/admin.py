from django.contrib import admin
from .models import Question, Quiztest, Reponses, Devoir, Utilisateur, Progres

# Register your models here.
class ReponsesAdmin(admin.TabularInline):
    model = Reponses
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets =[
        (None,  
            {'fields': ['type_question',('difficulty','note')]}),

        ("Contenu", 
            {
                'fields':['question_text','image']}),
    ]
    inlines = [ReponsesAdmin]
    list_filter=['type_question','difficulty']
    list_display=['__str__','type_question','difficulty','note']

class DevoirAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
            {'fields':[('type_devoir','difficulty_devoir')]}),
        ("Contenu",
            {'fields':['duree','contenu','texte']}),
    ]
    list_filter=['difficulty_devoir','type_devoir','duree']
    list_display=('difficulty_devoir','type_devoir','duree')

class UtilisateurAdmin(admin.ModelAdmin):
    list_display=['user','niveau_actuel','score_actuel']
    list_filter=['niveau_actuel','score_actuel']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiztest)
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Devoir, DevoirAdmin)
admin.site.register(Progres)