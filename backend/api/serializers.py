from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('username','email','password','password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self,attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password does not match"})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,attrs):
        
        user = authenticate(
            email=attrs["email"],
            password=attrs["password"]
        )
        if not user:
            raise serializers.ValidationError(
                "Usuário ou senha inválidos"
            )
        attrs["user"] = user
        return attrs