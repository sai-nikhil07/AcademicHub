# students/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Admin Actions
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    
    # ... existing paths ...
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
]