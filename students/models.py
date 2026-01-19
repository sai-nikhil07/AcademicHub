# students/models.py
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    BRANCH_CHOICES = [
        ('BCA', 'BCA'),
        ('B.Tech', 'B.Tech'),
        ('B.Sc', 'B.Sc'),
        ('BBA', 'BBA'),
    ]
    
    # Link to the standard Django User (handles username/password)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.roll_number})"