def evaluate_level(score):
    """Evaluate level base on score"""
    assert 0<= score <=10
    if score < 3:
        return "Débutant"
    elif score < 6:
        return "Moyen"
    elif score < 9:
        return "Avancé"
    else:
        return "Expert"

def get_user_answers(request):
    """"Returns a list of user answers"""
    return [ (k if v=='on' else v) for k,v in request.POST.items() if 'csrfmiddle' not in k][:-1]
