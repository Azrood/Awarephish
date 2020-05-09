def evaluate_level(score):
    """Evaluate level base on score"""
    assert 0<= score <=10
    if score < 3:
        return "Niveau 1"
    elif score < 6:
        return "Niveau 2"
    elif score < 9:
        return "Niveau 3"
    else:
        return "advanced"

def get_user_answers(request):
    """"Returns a list of user answers"""
    return [ (k if v=='on' else v) for k,v in request.POST.items() if 'csrfmiddle' not in k][:-1]

def message_level(level:str):
    if level == "Niveau 1":
        return "Attention votre score est assez bas, vous tombez facilement dans le piège, nous vous conseillons fortement de vous inscrire pour améliorer votre niveau"
    elif level == "Niveau 2":
        return "Votre score est moyen, nous vous conseillons de lire nos conseils et de vous inscrire pour améliorer votre niveau et ne plus tomber dans le piège des cybercriminels"
    elif level == "Niveau 3":
        return "Vous avez un bon score, vous tombez rarement dans le piège, nous vous conseillons toutefois de vous inscrire ou de lire nos conseils pour rester sur vos gardes."