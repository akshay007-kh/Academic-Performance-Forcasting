from django.contrib import admin
from django.urls import path
from core import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "staff-dashboard/",
        views.staff_dashboard,
        name="staff_dashboard"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
    path(
    "staff/",
    views.staff_list,
    name="staff_list"
    ),

    path(
        "staff/add/",
        views.add_staff,
        name="add_staff"
    ),
    path(
    "students/",
    views.student_list,
    name="student_list"
),

path(
    "students/add/",
    views.add_student,
    name="add_student"
),

path(
    "students/edit/<int:student_id>/",
    views.edit_student,
    name="edit_student"
),

path(
    "students/delete/<int:student_id>/",
    views.delete_student,
    name="delete_student"
),
path(
    "academic-records/",
    views.academic_records,
    name="academic_records"
),

path(
    "academic-records/add/",
    views.add_academic_record,
    name="add_academic_record"
),
path(
    "academic-records/edit/<int:record_id>/",
    views.edit_academic_record,
    name="edit_academic_record"
),

path(
    "academic-records/delete/<int:record_id>/",
    views.delete_academic_record,
    name="delete_academic_record"
),
path(
    "predict/<int:record_id>/",
    views.predict_performance,
    name="predict_performance"
),
path(
    "support-plan/add/<int:student_id>/",
    views.add_support_plan,
    name="add_support_plan"
),
path(
    "support-plans/",
    views.support_plans,
    name="support_plans"
),
path(
    "support-plans/edit/<int:plan_id>/",
    views.edit_support_plan,
    name="edit_support_plan"
),

path(
    "support-plans/delete/<int:plan_id>/",
    views.delete_support_plan,
    name="delete_support_plan"
),path(
    "high-risk-students/",
    views.high_risk_students,
    name="high_risk_students"
),
path(
    "prediction-history/",
    views.prediction_history,
    name="prediction_history"
),
path(
    "student-report/<int:student_id>/",
    views.student_report,
    name="student_report"
),
]