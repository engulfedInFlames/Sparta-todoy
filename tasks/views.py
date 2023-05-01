from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status

from .models import Task
from .serializers import TaskDetailSerializer


class TaskDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(Task, id=id)

    def get(self, request, id):
        task = self.get_object(id)
        serializer = TaskDetailSerializer(task)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        task = self.get_object(id)
        serializer = TaskDetailSerializer(
            task,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            task = serializer.save()
            serializer = TaskDetailSerializer(task)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        task = self.get_object(id)

        if task.user != request.user:
            raise NotAuthenticated

        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleCompletedOrNot(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        task = get_object_or_404(Task, id=id)

        if not request.user == task.user:
            raise NotAuthenticated

        task.is_completed = not task.is_completed
        task.save()

        return Response(status=status.HTTP_200_OK)
