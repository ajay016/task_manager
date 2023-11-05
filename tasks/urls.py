from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TaskList.as_view(), name='task_list'), 
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signout/', views.CustomLogoutView.as_view(), name='signout'),
    path('create_task/', views.CreateTask.as_view(), name='create_task'),
    path('save_task/', views.SaveTask.as_view(), name='save_task'),
    path('task_list/', views.TaskList.as_view(), name='task_list'),
    path('update_task_status/<int:task_id>/', views.UpdateTaskStatus.as_view(), name='update_task_status'),
    path('delete_task/<int:task_id>/', views.DeleteTask.as_view(), name='delete_task'),
    path('task_detail/<int:task_id>/', views.TaskDetailView.as_view(), name='task_detail'),
]
