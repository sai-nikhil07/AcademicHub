import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import Student, Course
from .forms import StudentRegistrationForm, CourseForm, StudentEditForm

# --- Helper Function ---
def is_admin(user):
    return user.is_superuser

# --- Auth Views ---
def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            login(request, student.user)
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'form': form})

# --- Dashboard (Router) ---
@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        return admin_dashboard(request)
    else:
        return student_dashboard(request)

def student_dashboard(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        student = None
    return render(request, 'students/dashboard_student.html', {'student': student})

# --- Admin Dashboard (Main Logic) ---
@user_passes_test(is_admin)
def admin_dashboard(request):
    # 1. Start with all data
    students = Student.objects.all()
    courses = Course.objects.all()
    
    # 2. Search Logic
    query = request.GET.get('q')
    if query:
        students = students.filter(
            Q(roll_number__icontains=query) | 
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )

    # 3. Handle Forms (Add Course / Add Student)
    course_form = CourseForm()
    student_form = StudentRegistrationForm()

    if request.method == 'POST':
        if 'add_course' in request.POST:
            course_form = CourseForm(request.POST)
            if course_form.is_valid():
                course_form.save()
                return redirect('dashboard')
        
        elif 'add_student' in request.POST:
            student_form = StudentRegistrationForm(request.POST)
            if student_form.is_valid():
                student_form.save()
                return redirect('dashboard')

    return render(request, 'students/dashboard_admin.html', {
        'students': students, 
        'courses': courses,
        'course_form': course_form,
        'student_form': student_form
    })

# --- Admin Actions ---
@user_passes_test(is_admin)
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    student.delete()
    user.delete() # Clean up the User account too
    return redirect('dashboard')

@user_passes_test(is_admin)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('dashboard')

@user_passes_test(is_admin)
def export_students(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Roll No', 'First Name', 'Last Name', 'Branch', 'Course']) # Header

    students = Student.objects.all().values_list(
        'roll_number', 'user__first_name', 'user__last_name', 'branch', 'course__name'
    )
    for std in students:
        writer.writerow(std)

@user_passes_test(is_admin)
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user

    if request.method == 'POST':
        # Use the specific Edit Form (No password required)
        form = StudentEditForm(request.POST, instance=student)
        
        if form.is_valid():
            # 1. Save Student Model (Branch, Course, Roll No)
            student = form.save()

            # 2. Update User Model (Name, Email) manually
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            return redirect('dashboard')
    else:
        # Pre-fill the form with existing User data
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        form = StudentEditForm(instance=student, initial=initial_data)

    return render(request, 'students/edit_student.html', {'form': form, 'student': student})

    return response