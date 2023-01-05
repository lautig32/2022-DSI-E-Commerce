from rest_framework import serializers
from user.models import *

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'document_number', 'number_phone',
                    'address', 'number_adress', 'is_active', 'description')