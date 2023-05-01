from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

from .models import CustomUser
from .forms import SignupForm, LoginForm
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    CreateUserSerializer,
)


class Users(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(
            users,
            many=True,
        )

        return Response(serializer.dataa, status=status.HTTP_200_OK)


class Me(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        serializer = UserDetailSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserDetailSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Signup(APIView):
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")

        form = SignupForm()
        url = request.get_full_path()
        context = {
            "form": form,
            "url": url,
        }

        return render(request, "users/signup.html", context=context)
    """

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is None:
            raise AuthenticationFailed

        login(request, user=user)

        return Response(status=status.HTTP_200_OK)


class Logout(APIView):
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
