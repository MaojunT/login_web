from django import forms
from django.contrib.auth.models import User
from . import models
 
class UserForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="comfirm password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={'class': 'form-control'}))

class UpdateEmailForm(forms.ModelForm):
    email = forms.EmailField(label="new email",required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
    	model = User
    	fields = ('email',)

class UpdatePwdForm(forms.ModelForm):
	oldpwd = forms.CharField(label="old password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	newpwd = forms.CharField(label="new password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	cfmpwd = forms.CharField(label="comfirm password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('password',)

class UserChoice(forms.Form):
    username = forms.CharField(max_length=128)
    choice_1 = forms.CharField(max_length = 64)
    choice_2 = forms.CharField(max_length = 64)
    choice_3 = forms.CharField(max_length = 64)