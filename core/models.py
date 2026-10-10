from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    view_pass = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    batch = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student_id} - {self.name}"


class AcademicRecord(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="academic_records"
    )

    semester = models.IntegerField()
    attendance = models.FloatField()
    internal_marks = models.FloatField()
    assignment_marks = models.FloatField()
    previous_marks = models.FloatField()
    study_hours = models.FloatField()
    backlogs = models.IntegerField(default=0)
    participation = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - Semester {self.semester}"


class Prediction(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="predictions"
    )

    academic_record = models.ForeignKey(
        AcademicRecord,
        on_delete=models.CASCADE
    )

    predicted_mark = models.FloatField()

    performance = models.CharField(max_length=20)

    risk_level = models.CharField(max_length=20)

    predicted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.predicted_mark}"


class SupportPlan(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="support_plans"
    )

    support_type = models.CharField(max_length=100)

    problem = models.TextField()

    action_taken = models.TextField()

    assigned_staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Ongoing", "Ongoing"),
            ("Completed", "Completed"),
        ],
        default="Pending"
    )

    follow_up_date = models.DateField(null=True, blank=True)

    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.support_type}"