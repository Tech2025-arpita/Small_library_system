from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=['auth_id', 'auth_name','created_at','updated_at']
        read_only_fields=['auth_id','created_at','updated_at']



