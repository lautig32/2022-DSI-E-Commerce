from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from user.models import *



class SignUpForm(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 
                'password1', 'password2', 'document_number',
                'address', 'number_adress', 'number_phone',)

class EditMyProfileForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    document_number = forms.CharField(required=False)
    address = forms.CharField(required=False)
    number_adress = forms.IntegerField(required=False)
    number_phone = forms.IntegerField(required=False)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'document_number',
                'address', 'number_adress', 'number_phone',)
                # 'email', password1',
        exclude = ('email', 'password1', 'password2')