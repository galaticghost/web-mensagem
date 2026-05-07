from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from .models import User

class UserRegisterView(views.APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response({
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(views.APIView):
    pass