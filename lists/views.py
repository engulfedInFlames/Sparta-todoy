from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.views import APIView

from .models import List
from .serializers import ListsSerializer, ListDetailSerializer, CreateListSerializer
from tasks.serializers import CreateTaskSerializer


class Lists(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        lists = request.user.lists
        serializer = ListsSerializer(lists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateListSerializer(data=request.data)

        if serializer.is_valid():
            list = serializer.save(user=request.user)
            serializer = ListDetailSerializer(list)

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(List, id=id)

    def get(self, request, id):
        list = self.get_object(id)
        serializer = ListDetailSerializer(list)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        list = self.get_object(id)
        serializer = ListDetailSerializer(
            list,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            list = serializer.save()
            serializer = ListDetailSerializer(list)

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        list = self.get_object(id)
        list.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateTask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        list = get_object_or_404(List, id=id)
        serializer = CreateTaskSerializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save(
                user=request.user,
                list_id=id,
            )
            list.tasks.add(task)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
