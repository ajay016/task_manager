from django.contrib import admin
from django.urls import path, include
from . import views
from . import apiViews

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
    path('task_update/<int:task_id>/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task_update_save/<int:task_id>/', views.TaskUpdate.as_view(), name='task_update_save'),

    # API views
    # path('api/', apiViews.apiOverview, name="api"),
    path('api/task_list/', apiViews.TaskListApiView.as_view(), name="api_task_list"),
    path('api/task_detail/<int:task_id>/', apiViews.TaskDetailApiView.as_view(), name="api_task_detail"),
    path('api/task_create/', apiViews.TaskCreateApiView.as_view(), name="api_task_create"),
    # path('api/api_task_create/', apiViews.TaskCreateApiView.as_view(), name="api_task_create"),
    path('api/task_update/<int:task_id>/', apiViews.TaskUpdateApiView.as_view(), name="api_task_update"),
    path('api/task_update_patch/<int:task_id>/', apiViews.TaskPatchApiView.as_view(), name="api_task_update_patch"),
    path('api/task_delete/<int:task_id>/', apiViews.TaskDeleteApiView.as_view(), name="task_delete"),
]
