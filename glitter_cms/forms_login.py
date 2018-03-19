from django import forms
from django.contrib.auth.models import User
from glitter_cms.models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(forms.ModelForm):
    student_id = forms.CharField(max_length=8, required=True, help_text='Required U of Glasgow student ID. Example: 2349514c')

    class Meta:
        model = Profile
        fields = ('student_id',)


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, help_text='required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )