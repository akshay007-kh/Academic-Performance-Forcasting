from django.contrib import admin
from .models import Staff, Student, AcademicRecord, Prediction, SupportPlan


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'phone')
    search_fields = ('name', 'department')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'name',
        'course',
        'department',
        'semester',
        'batch'
    )
    search_fields = ('student_id', 'name', 'department')
    list_filter = ('department', 'semester', 'course')


@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'semester',
        'attendance',
        'internal_marks',
        'assignment_marks',
        'previous_marks',
        'backlogs'
    )
    list_filter = ('semester',)
    search_fields = ('student__name', 'student__student_id')


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'predicted_mark',
        'performance',
        'risk_level',
        'predicted_at'
    )
    list_filter = ('performance', 'risk_level')
    search_fields = ('student__name', 'student__student_id')


@admin.register(SupportPlan)
class SupportPlanAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'support_type',
        'assigned_staff',
        'status',
        'follow_up_date'
    )
    list_filter = ('status', 'support_type')
    search_fields = ('student__name', 'student__student_id')