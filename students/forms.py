# students/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Student, Course

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = ['roll_number', 'branch', 'course']

    def save(self, commit=True):
        # Save User first
        user = User.objects.create_user(
            username=self.cleaned_data['roll_number'], # Using Roll No as Username
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        # Save Student profile
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']

# Open students/forms.py and ADD this class at the bottom

class StudentEditForm(forms.ModelForm):
    # These fields are for the User model, so we define them explicitly here
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = ['roll_number', 'branch', 'course']
