from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import *

from django.utils.translation import gettext_lazy as _


class UserProfileForm(UserCreationForm):

    password1 = forms.CharField(label='Password', widget = forms.PasswordInput(
        attrs ={
            'class': 'form-control',
            'placeholder': _('Enter password'),
            'id': 'password1',
            'required':'required',
        }
    ))

    password2 = forms.CharField(label='Confirmation password', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('Re-enter password'),
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 
                'password1', 'password2', 'document_number',
                'address', 'number_adress', 'number_phone',)
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('First name'),
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Last name'),
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': _('Email address'),
                    'required': 'required',
                }
            ),
            'document_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Document'),
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Address'),
                }
            ),
            'number_adress': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Number address'),
                }
            ),
            'number_phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Number phone'),
                }
            ),            
        }


class EditMyProfileForm(UserProfileForm):

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'document_number',
                'address', 'number_adress', 'number_phone',)
        excludes = ('email', 'password1', 'password2')


class UserProfileAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileAuthenticationForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = _('Email addres')
        self.fields['username'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = _('Password')
        self.fields['password'].widget.attrs['autocomplete'] = 'new-password'