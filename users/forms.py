from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from users.models import User, Group


class SignUpForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)

    def __int__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = None

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        email = self.cleaned_data['email']

        if username and password and repeat_password and email:
            if password == repeat_password:
                encrypt_password = make_password(password)
                if User.objects.filter(username=username).exists():
                    raise ValidationError(_('User is already exist, try to change username'))
                else:
                    self.user = User(password=encrypt_password, email=email, username=username)
                    self.user.save()
            else:
                raise ValidationError(_('Passwords not match'))

    def get_user(self):
        return self.user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = None

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = authenticate(self.request, username=username, password=password)

        if self.user is None:
            raise ValidationError(
                ValidationError(_('Problem with password or username')),
            )
        if not self.user.is_active:
            raise ValidationError(
                ValidationError(_('This user is no longer active'))
            )

        return self.cleaned_data

    def get_user(self):
        return self.user


class GroupCreatingForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'description']

    def __int__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def save_group(self, commit=True):
        created_group = Group(
            group_name=self.cleaned_data['group_name'],
            description=self.cleaned_data['description'],
        )

        created_group.save()


class UserCreatingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def __int__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def save_user(self, group_id):
        created_user = User(
            username=self.cleaned_data['username'],
            group_id_id=group_id,
        )

        created_user.save()