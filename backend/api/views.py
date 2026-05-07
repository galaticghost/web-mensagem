from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterView(views.APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )