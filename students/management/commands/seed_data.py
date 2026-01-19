# students/management/commands/seed_data.py
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student, Course

class Command(BaseCommand):
    help = 'Populate database with 30 dummy Indian students'

    def handle(self, *args, **kwargs):
        # 1. Create Courses
        courses = ['Data Science', 'Web Dev', 'Cloud Computing', 'AI Basics']
        course_objs = []
        for c in courses:
            obj, _ = Course.objects.get_or_create(name=c)
            course_objs.append(obj)
        
        self.stdout.write("Courses created.")

        # 2. Indian Names Data
        first_names = ["Aarav", "Vihaan", "Aditya", "Sai", "Rohan", "Priya", "Ananya", "Diya", "Isha", "Riya", 
                       "Karan", "Arjun", "Vikram", "Rahul", "Nisha", "Sanya", "Sneha", "Amit", "Suresh", "Pooja",
                       "Manoj", "Kavita", "Raj", "Simran", "Varun", "Neha", "Deepak", "Anjali", "Meera", "Yash"]
        last_names = ["Sharma", "Verma", "Gupta", "Patel", "Reddy", "Singh", "Kumar", "Das", "Nair", "Rao"]

        # 3. Create 30 Students
        count = 0
        for i in range(30):
            fname = first_names[i % len(first_names)]
            lname = random.choice(last_names)
            username = f"std{100+i}"
            
            # Avoid duplicates if running script twice
            if User.objects.filter(username=username).exists():
                continue

            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="password123",
                first_name=fname,
                last_name=lname
            )

            Student.objects.create(
                user=user,
                roll_number=f"BCA2025-{100+i}",
                branch="BCA",  # As requested
                course=random.choice(course_objs)
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} new students.'))