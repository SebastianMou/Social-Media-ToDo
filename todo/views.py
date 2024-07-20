from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Task, TaskFolder
from .forms import TaskFolderForm, TaskForm, TaskSearchForm, UserRegisterForm
#tests
# Create your views here.
def hero(request):
    return render(request, 'hero.html')

@login_required
def home(request):
    tasks = TaskFolder.objects.filter(owner=request.user)
    if request.method == 'POST':
        form = TaskFolderForm(request.POST)
        if form.is_valid():
            task_folder = form.save(commit=False)
            task_folder.owner = request.user
            task_folder.save()
            return redirect('home')
    else:
        form = TaskFolderForm()
    
    context = {
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'home.html', context)

def search_personal_task(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        tasks = Task.objects.filter(title__icontains=searched, owner=request.user)
    else:
        searched = ""
        tasks = []

    context = {
        'searched': searched,
        'tasks': tasks,
    }
    return render(request, 'tasks/search_results.html', context)

def search_all(request):
    tasks = []
    searched = ""
    if request.method == 'POST':
        searched = request.POST.get('searched', '')
        tasks = Task.objects.filter(title__icontains=searched, publ_or_priv=True)
    
    context = {
        'searched': searched,
        'tasks': tasks,
    }
    return render(request, 'tasks/search_all.html', context)

def folder_detail(request, pk):
    task_folder = get_object_or_404(TaskFolder, pk=pk)
    tasks = task_folder.tasks.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.folder = task_folder
            task.owner = request.user
            task.save()
            return redirect('folder_detail', pk=task_folder.pk)
    else:
        form = TaskForm()

    context = {
        'task_folder': task_folder,
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'folder_detail.html', context)

@login_required
def toggle_task_completion(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('folder_detail', pk=task.folder.pk)

def edit_task_folder(request, pk):
    task_folder = get_object_or_404(TaskFolder, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = TaskFolderForm(request.POST, instance=task_folder)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskFolderForm(instance=task_folder)

    context = {
        'form': form,
        'task_folder': task_folder
    }
    return render(request, 'edit_task_folder.html', context)

def delete_task_folder(request, pk):
    task_folder = get_object_or_404(TaskFolder, pk=pk, owner=request.user)
    task_folder.delete()
    return redirect('home')

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.publ_or_priv or task.owner == request.user:
        context = {
            'task': task,
        }
        return render(request, 'tasks/task_detail.html', context)
    else:
        return render(request, '404.html', status=404)  # Custom 404 page or raise Http404


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('folder_detail', args=[task.folder.pk]))

    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'task': task,
    }
    return render(request, 'tasks/task_edit.html', context)

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.delete()
    return redirect(reverse('folder_detail', args=[task.folder.pk]))

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = UserRegisterForm()
    return render(request, 'authentication/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('home')  # Redirect to the home page or any other page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')