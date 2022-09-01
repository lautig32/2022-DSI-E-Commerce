from django.contrib.auth.forms import UserCreationForm

from user.models import *



class SignUpForm(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 
                'password1', 'password2', 'document_number',
                'address', 'number_adress', 'number_phone',)