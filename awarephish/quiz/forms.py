from django import forms
from .models import Utilisateur,User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d\'utilisateur', widget=forms.TextInput(attrs={'placeholder':'Entrez le nom d\'utilisateur'}))
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'placeholder':'Entrez votre mot de passe'}))
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput(attrs={'placeholder':'Confirmer votre mot de passe'}))
    email = forms.EmailField(label='Adresse Email',widget=forms.EmailInput(attrs={'placeholder':'Entrez votre email'}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Utilisateur.user.get_queryset().filter(username=username)
        if r.count():
            raise ValidationError("Nom d'utilisateur déjà pris")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Utilisateur.user.get_queryset().filter(email=email)
        if r.count():
            raise ValidationError("Cette adresse existe déjà")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passes ne correspondent pas")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class SigninForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Nom d\'utilisateur', widget=forms.TextInput(attrs={'placeholder':'Entrez le nom d\'utilisateur'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'placeholder':'Entrez votre mot de passe'}))

    error_messages = {
        'invalid_login': ("Nom d`'utilisateur ou mot de passe incorrect"),
    }

class ChangePass(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder':'Entrez votre nouveau mot de passe'}),
        strip=False,
        help_text="Au minimum 8 caractères.\nDoit contenir au moins un caractère numérique, une majuscule et un symbole",
    )
    new_password2 = forms.CharField(
        label="Confirmation du nouveau mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder':'Confirmer votre nouveau mot de passe'}),
    )
    old_password = forms.CharField(
        label="Mot de passe actuel",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,'placeholder':'Entrer votre mot de passe actuel'})
    )

    error_messages = {
        'password_mismatch':('Les mots de passe ne correspondent pas'),
        'password_incorrect':("Votre ancien mot de passe est incorrect"),
    }

class ChangeMail(forms.Form):
    error_messages={
        'email_inuse': "Cette adresse est déjà enregistrée.",
        'password_incorrect': 'Mot de passe incorrect'
}

    old_mail = forms.EmailField(label='Adresse Email actuelle',widget=forms.EmailInput(attrs={'placeholder':'Entrer votre adresse actuelle'}))
    new_email = forms.EmailField(label='Nouvelle adresse Email',widget=forms.EmailInput(attrs={'placeholder':'Entrez votre nouvelle adresse email'}))
    current_password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'placeholder':'entrez votre mot de passe pour confirmer'}),required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeMail, self).__init__(*args, **kwargs)
    
    def clean_current_password(self):
        """
        Validates that the password field is correct.
        """
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise forms.ValidationError(self.error_messages['password_incorrect'], code='password_incorrect',)
        return current_password