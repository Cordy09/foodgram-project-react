from recipes.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', )
        model = User
    
