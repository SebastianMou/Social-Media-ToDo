from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hero, name='hero'),
    path('home/', views.home, name='home'),
    path('folder_detail/<str:pk>/', views.folder_detail, name='folder_detail'),
    path('edit_task_folder/<int:pk>/', views.edit_task_folder, name='edit_task_folder'),
    path('delete_task_folder/<int:pk>/', views.delete_task_folder, name='delete_task_folder'),
    path('task/toggle/<int:pk>/', views.toggle_task_completion, name='toggle_task_completion'),

    path('task_detail/<int:pk>/', views.task_detail, name='task_detail'),
    path('task_edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('task_delete/<int:pk>/', views.task_delete, name='task_delete'),
    
    path('search_personal_task/', views.search_personal_task, name='search_personal_task'),
    path('search_all/', views.search_all, name='search_all'),

    path('register/', views.register, name='register'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('login/', views.custom_login, name='login'),

    # Forgoten password 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_management/password_reset.html'), name="password_reset"),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_management/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_management/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_management/password_reset_complete.html'), name='password_reset_complete'),
]