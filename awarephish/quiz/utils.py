def evaluate_level(score):
    """Evaluate level base on score"""
    assert 0<= score <=300
    if score < 100:
        return "Niveau 1"
    elif score < 200:
        return "Niveau 2"
    elif score <= 300:
        return "Niveau 3"

def get_nextlevel_score(curr_level):
    """Return necessary score for next level"""
    if curr_level == "Niveau 1":
        return 100
    elif curr_level == "Niveau 2":
        return 200
    elif curr_level == "Niveau 3":
        return 300


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

def evaluate_level_test(score):
    assert 0<= score <= 10
    if score < 3:
        return "Niveau 1"
    elif score < 6:
        return "Niveau 2"
    else:
        return "Niveau 3"