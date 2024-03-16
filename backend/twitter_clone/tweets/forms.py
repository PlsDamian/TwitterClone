from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Tweet


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username', 'avatar', 'display_name', 'user_id', 'bio']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_id': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Make specific fields optional
        self.fields['avatar'].required = False
        self.fields['display_name'].required = False
        self.fields['user_id'].required = False
        self.fields['bio'].required = False


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content', 'media']
