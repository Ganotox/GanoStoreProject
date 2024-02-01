from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import User, Program, Comment, Complaint, Rating

User = get_user_model()


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']


class CustomUserCreationForm(UserCreationForm):
    secret_question = forms.CharField(required=True)
    secret_answer = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'avatar', 'password1', 'password2', 'secret_question', 'secret_answer')


class ProgramUploadForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('title', 'description', 'category', 'genre', 'program_file', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('content',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Введіть адресу електронної пошти, повязану з вашим акаунтом.')


class SecretQuestionAnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.PasswordInput, label="Відповідь на секретне питання")


class RatingForm(forms.ModelForm):
    score = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                               widget=forms.NumberInput(attrs={'type': 'number', 'min': '1', 'max': '5'}))

    class Meta:
        model = Rating
        fields = ['score']
