from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, PasswordInput, FileInput

from main.models import Courses


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

    def clean(self):
        super(UserCreationForm, self).clean()

        # getting username and password from cleaned_data
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # validating the username and password
        if len(username) < 5:
            self._errors['username'] = self.error_class(['A minimum of 5 characters is required'])

        if len(password) < 8:
            self._errors['password'] = self.error_class(['Password length should not be less than 8 characters'])

        return self.cleaned_data


class CourseCreationForm(ModelForm):
    class Meta:
        model = Courses
        fields = ['title', 'author', 'description', 'price', 'image']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course title'
            }),
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Author'
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description'
            }),
            'price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price'
            }),
            'image': FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'image'
            })

        }

class CourseSearchForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    author = forms.CharField(max_length=50, required=False)
    price_min = forms.FloatField(required=False)
    price_max = forms.FloatField(required=False)
    published_only = forms.BooleanField(required=False)

    class Meta:
        fields = ['title', 'author', 'price_min', 'price_max', 'published_only']