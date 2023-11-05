from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
import environ
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_api_key.models import APIKey
from rest_framework.permissions import IsAuthenticated
# from rest_framework_api_key.permissions import HasAPIKey 
from .models import *
from .serializers import TaskSerializer
from rest_framework.renderers import TemplateHTMLRenderer
# from .permissions import Check_API_KEY_Auth
import requests


class TaskListApiView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        env = environ.Env()
        environ.Env.read_env()
        api_key = env('API_KEY')
        print('api key: ', api_key)
        api_header = request.headers
        api_get_header = request.headers.get('Api-Key')

        if api_key == api_get_header:
            print('api_header: ', api_header)
            print('api_get_header: ', api_get_header)

            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)

            return Response(serializer.data)
        
        # else:
        #     return Response({'message': 'Access Denied'})


class TaskDetailApiView(APIView):
    def get(self, request, task_id):
        if request.user.is_authenticated:
            tasks = Task.objects.get(id=task_id)
            serializer = TaskSerializer(tasks)

            return Response(serializer.data)
        
        else:
            return Response({'message': 'Access Denied'}) 
    

class TaskCreateApiView(APIView):
    # def get(self, request):
    #     serializer = TaskSerializer()
    #     return render(request, 'tasks/api_task_create.html', {'serializer': serializer})
    
    def post(self, request):
        if request.user.is_authenticated:
            serializer = TaskSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Task created succesfully'}, status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({'message': 'Access Denied'})
        

class TaskUpdateApiView(APIView):
    def put(self, request, task_id):
        if request.user.is_authenticated:
            task = Task.objects.get(id=task_id)
            serializer = TaskSerializer(task, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Task updated succesfully'}, status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({'message': 'Access Denied'})
        

class TaskPatchApiView(APIView):
    def patch(self, request, task_id):
        if request.user.is_authenticated:
            task = Task.objects.get(id=task_id)
            serializer = TaskSerializer(task, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Task updated succesfully'}, status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({'message': 'Access Denied'})
        

class TaskDeleteApiView(APIView):
    def delete(self, request, task_id):
        if request.user.is_authenticated:
            task = Task.objects.get(id=task_id)
            task.delete()

            return Response({'message': 'Task deleted'})
        
        else:
            return Response({'message': 'Access Denied'})
