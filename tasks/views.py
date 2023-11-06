from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from .forms import TaskForm
from django.shortcuts import render, get_object_or_404
from .filters import TaskFilter
import json
from datetime import datetime
from .models import *
from .forms import *

# Create your views here.
class HomeView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "home"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        # Render the template with the context data
        return render(request, 'tasks/home.html')
    

class SignUpView(View):
    def get(self, request):
        return render(request, 'tasks/signup.html')

    def post(self, request):
        if request.method == 'POST':
            # username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            print('first_name: ', first_name)
            print('email: ', email)

            if not first_name or not last_name or not email or not password or not confirm_password:
                return JsonResponse({'error_missing_fields': 'All fields are required'})

            else:
                if password != confirm_password:
                    return JsonResponse({'error_password': 'Passwords do not match'})

                # checks if any user with the entered email or username exists
                # if User.objects.filter(username=username).exists():
                #     return JsonResponse({'error_email': 'Username is not available'})
                
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'error_email': 'Email already exists'})
                
                
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email)
                user.set_password(password)
                user.save()

                # login(request, user)  # Log the user in
                return JsonResponse({'success': True})  # Redirect to the home page or any other desired page
        

class LoginView(LoginView):
    template_name = 'tasks/login.html'  # Replace with the path to your login template
    success_template_name = 'success.html'  # Replace with the path to your success template
    redirect_authenticated_user = True

    def get(self, request):
        user = request.user
        print('user before: ', user)
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        print('email: ', email)
        print('password: ', password)

        user = authenticate(request, email=email, password=password)
        print('user: ', user)

        if user is not None:
            login(request, user)
            # Render a success template upon successful login
            return redirect('task_list')
        else:
            # Authentication failed, handle it accordingly
            return render(request, self.template_name, {'error_message': 'Invalid email or password'})
        

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class CreateTask(CreateView):
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'tasks/create_task.html')
    model = Task
    template_name = 'tasks/create_task.html'
    context_object_name = 'tasks'
    fields = ['title', 'description', 'due_date', 'priority', 'photos']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['priorities'] = [
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
        ]
        print('context: ', context)
        return context
    

class SaveTask(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        title = request.POST.get('task_name')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        photos = request.FILES.getlist('photos')

        saved_photos = []  # To store saved Photo objects

        if due_date:
            try:
                formatted_date = datetime.strptime(due_date, "%b. %d, %Y").strftime("%Y-%m-%d")
            except ValueError:
                try:
                    formatted_date = datetime.strptime(due_date, '%Y-%m-%d')
                except:
                    JsonResponse({'error_date': 'Error Parsing Date'} )
        
        else:
            formatted_date = None

        if title == '':
            print('null')
            return JsonResponse({'error_title': 'Title is required'})

        else:
            for photo in photos:
                new_photo = Photo(image=photo)
                new_photo.save()
                saved_photos.append(new_photo)

            task = Task(user=user, title=title, description=description, due_date=formatted_date, priority=priority)

            task.save()
            task.photos.set(saved_photos)
            return JsonResponse({'success': True})
        

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    filter_task = TaskFilter
    context_object_name = 'tasks'   # in the template 'task_list' we can write tasks instead of object_list
    # is_complete = django_filters.BooleanFilter()

    def get_queryset(self):
        # Filter the tasks based on the user
        queryset = super().get_queryset().filter(user=self.request.user)
        
        # Apply the filters from the request using django-filter
        filterset = self.filter_task(data=self.request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        return queryset

    # User gets only their data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('Context:', context)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        # context['count'] = context['tasks'].filter(complete=False).count()
        context['filterset'] = self.filter_task

        print(context['tasks'])
        filter_options = ['Creation Date',
            'Due Date',
            'Priority',
            'Completed',
            ]
            
        # context['filter_options'] = filter_options

        # Search function
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            # the name of the task is returned as we search. The search in the search-area field is matched
            # with the title using 'title__icontains'
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            # 'title__startswith' filters the search that starts with thw word that we search
            # context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            context['search_input'] = search_input

        return context
    

class UpdateTaskStatus(View):
    def post(self, request, task_id):
        if request.user.is_authenticated:
            data = json.loads(self.request.body)
            print('data: ', data)
            try:
                task = Task.objects.get(id=task_id, user=request.user)
                is_complete = data['completed']
                if is_complete is True:
                    print('is_completed: ', is_complete)
                    task.is_complete = is_complete
                    task.save()
                    return JsonResponse({'success': 'Task status updated to Completed'})
                else:
                    print('is_completed: ', is_complete)
                    task.is_complete = is_complete
                    task.save()
                    return JsonResponse({'success': 'Task status updated to Pending'})
            except Task.DoesNotExist:
                return JsonResponse({'error_task': 'Task not found'}, status=404)
            
        else:
            return JsonResponse({'error_user': 'Access denied'})
        

class DeleteTask(View):
    def post(self, request, task_id):
        if request.user.is_authenticated:
            try:
                task = Task.objects.get(id=task_id, user=request.user)
                print('task id: ', task_id)
                task.delete()
                return JsonResponse({'success': 'Task deleted successfully'})
            except Task.DoesNotExist:
                return JsonResponse({'error': 'Task not found'}, status=404)
            
        else:
            return JsonResponse({'error_user': 'Access denied'})
        

class TaskDetailView(View):
    template_name = 'tasks/task_detail.html'

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)  # Retrieve the task by primary key
        context = {'task': task}
        return render(request, self.template_name, context)
        

class TaskUpdateView(View):
    template_name = 'tasks/task_update.html'  # Create a template for rendering the form

    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        context = {
            'task': task,
            'priorities': [
                ('Low', 'Low'),
                ('Medium', 'Medium'),
                ('High', 'High'),
            ]
        }
        print('context: ', context)
        return render(request, self.template_name, context)

    # def post(self, request, task_id):
    #     task = Task.objects.get(id=task_id)

    #     # Update the task fields based on POST data
    #     task.title = request.POST.get('title')
    #     task.description = request.POST.get('description')
    #     task.due_date = request.POST.get('due_date')

    #     task.save()  # Save the updated task

    #     return redirect('task-list')  # Redirect to a success URL upon updating
    

class TaskUpdate(View):
    def post(slef, request, task_id):
        task = Task.objects.get(id=task_id)

        title = request.POST.get('task_name')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        print('title: ', title)

        photo_id_list = request.POST.get('photo_id_list')
        photo_id_list = photo_id_list.split(',')
        new_photos = request.FILES.getlist('photos')
        print('add_photo_list: ', new_photos)
        
        print('photo_id_list: ', photo_id_list)

        if due_date:
            try:
                formatted_date = datetime.strptime(due_date, "%b. %d, %Y").strftime("%Y-%m-%d")
            except ValueError:
                try:
                    formatted_date = datetime.strptime(due_date, '%Y-%m-%d')
                except:
                    JsonResponse({'error_date': 'Error Parsing Date'} )
        
        else:
            formatted_date = None


        if title == '':
            print('null')
            return JsonResponse({'error_title': 'Title is required'})
        
        else:
            photos = []
            for photo_id in photo_id_list:
                try:
                    photo = Photo.objects.get(id=photo_id)
                    print('got photo: ', photo.id)
                    print('photo.task_set: ', photo.task_set.all())
                    task.photos.remove(photo)
                    photo.task_set.remove(task)
                    print('photo.task_set1: ', photo.task_set.all())
                except:
                    photo = None
                    print('no photo')

            for new_photo in new_photos:
                photo = Photo(image=new_photo)
                photo.save()
                task.photos.add(photo)

            task.title = title
            task.description = description
            task.due_date = formatted_date
            task.priority = priority
            task.save()

            return JsonResponse({'success': 'Task Updated Successfully'})

        
