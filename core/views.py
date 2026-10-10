from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import *

import joblib
import pandas as pd
from pathlib import Path


# =========================================================
# ML MODEL
# =========================================================

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "ml"
    / "performance_model.pkl"
)

model = joblib.load(MODEL_PATH)


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(request, "home.html")


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")

            else:
                return redirect("staff_dashboard")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid username or password"
            }
        )

    return render(request, "login.html")


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard(request):

    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("login")

    total_staff = Staff.objects.count()

    total_students = Student.objects.count()

    high_risk = Prediction.objects.filter(
        risk_level="High"
    ).values("student").distinct().count()

    medium_risk = Prediction.objects.filter(
        risk_level="Medium"
    ).values("student").distinct().count()

    low_risk = Prediction.objects.filter(
        risk_level="Low"
    ).values("student").distinct().count()

    pending_support = SupportPlan.objects.filter(
        status="Pending"
    ).count()

    ongoing_support = SupportPlan.objects.filter(
        status="Ongoing"
    ).count()

    completed_support = SupportPlan.objects.filter(
        status="Completed"
    ).count()

    context = {
        "total_staff": total_staff,
        "total_students": total_students,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "pending_support": pending_support,
        "ongoing_support": ongoing_support,
        "completed_support": completed_support,
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )


# =========================================================
# STAFF DASHBOARD
# =========================================================

def staff_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    total_students = Student.objects.count()

    high_risk = Prediction.objects.filter(
        risk_level="High"
    ).values("student").distinct().count()

    medium_risk = Prediction.objects.filter(
        risk_level="Medium"
    ).values("student").distinct().count()

    low_risk = Prediction.objects.filter(
        risk_level="Low"
    ).values("student").distinct().count()

    pending_support = SupportPlan.objects.filter(
        status="Pending"
    ).count()

    ongoing_support = SupportPlan.objects.filter(
        status="Ongoing"
    ).count()

    context = {
        "total_students": total_students,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "pending_support": pending_support,
        "ongoing_support": ongoing_support,
    }

    return render(
        request,
        "staff_dashboard.html",
        context
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect("login")


# =========================================================
# STAFF MANAGEMENT
# =========================================================

def staff_list(request):

    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("login")

    staff_members = Staff.objects.select_related(
        "user"
    ).all()

    return render(
        request,
        "staff_list.html",
        {
            "staff_members": staff_members
        }
    )


def add_staff(request):

    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("login")

    if request.method == "POST":

        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        department = request.POST.get("department")

        if User.objects.filter(username=username).exists():

            return render(
                request,
                "add_staff.html",
                {
                    "error": "Username already exists"
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Staff.objects.create(
            user=user,
            name=name,
            phone=phone,
            department=department,
            view_pass=password
        )

        return redirect("staff_list")

    return render(request, "add_staff.html")


# =========================================================
# STUDENT MANAGEMENT
# =========================================================

def student_list(request):

    if not request.user.is_authenticated:
        return redirect("login")

    students = Student.objects.all().order_by("-id")

    return render(
        request,
        "student_list.html",
        {
            "students": students
        }
    )


def add_student(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        student_id = request.POST.get("student_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        course = request.POST.get("course")
        department = request.POST.get("department")
        semester = request.POST.get("semester")
        batch = request.POST.get("batch")

        if Student.objects.filter(
            student_id=student_id
        ).exists():

            return render(
                request,
                "add_student.html",
                {
                    "error": "Student ID already exists"
                }
            )

        Student.objects.create(
            student_id=student_id,
            name=name,
            email=email,
            phone=phone,
            course=course,
            department=department,
            semester=semester,
            batch=batch
        )

        return redirect("student_list")

    return render(
        request,
        "add_student.html"
    )


def edit_student(request, student_id):

    if not request.user.is_authenticated:
        return redirect("login")

    student = Student.objects.get(
        id=student_id
    )

    if request.method == "POST":

        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")
        student.course = request.POST.get("course")
        student.department = request.POST.get("department")
        student.semester = request.POST.get("semester")
        student.batch = request.POST.get("batch")

        student.save()

        return redirect("student_list")

    return render(
        request,
        "edit_student.html",
        {
            "student": student
        }
    )


def delete_student(request, student_id):

    if not request.user.is_authenticated:
        return redirect("login")

    student = Student.objects.get(
        id=student_id
    )

    student.delete()

    return redirect("student_list")


# =========================================================
# ACADEMIC RECORDS
# =========================================================

def academic_records(request):

    if not request.user.is_authenticated:
        return redirect("login")

    records = AcademicRecord.objects.select_related(
        "student"
    ).order_by("-created_at")

    return render(
        request,
        "academic_records.html",
        {
            "records": records
        }
    )


def add_academic_record(request):

    if not request.user.is_authenticated:
        return redirect("login")

    students = Student.objects.all().order_by("name")

    if request.method == "POST":

        student_id = request.POST.get("student")
        semester = request.POST.get("semester")
        attendance = request.POST.get("attendance")
        internal_marks = request.POST.get("internal_marks")
        assignment_marks = request.POST.get("assignment_marks")
        previous_marks = request.POST.get("previous_marks")
        study_hours = request.POST.get("study_hours")
        backlogs = request.POST.get("backlogs")
        participation = request.POST.get("participation")

        student = Student.objects.get(
            id=student_id
        )

        AcademicRecord.objects.create(
            student=student,
            semester=semester,
            attendance=attendance,
            internal_marks=internal_marks,
            assignment_marks=assignment_marks,
            previous_marks=previous_marks,
            study_hours=study_hours,
            backlogs=backlogs,
            participation=participation
        )

        return redirect("academic_records")

    return render(
        request,
        "add_academic_record.html",
        {
            "students": students
        }
    )


def edit_academic_record(request, record_id):

    if not request.user.is_authenticated:
        return redirect("login")

    record = AcademicRecord.objects.get(
        id=record_id
    )

    students = Student.objects.all().order_by("name")

    if request.method == "POST":

        record.student = Student.objects.get(
            id=request.POST.get("student")
        )

        record.semester = request.POST.get("semester")
        record.attendance = request.POST.get("attendance")
        record.internal_marks = request.POST.get("internal_marks")
        record.assignment_marks = request.POST.get("assignment_marks")
        record.previous_marks = request.POST.get("previous_marks")
        record.study_hours = request.POST.get("study_hours")
        record.backlogs = request.POST.get("backlogs")
        record.participation = request.POST.get("participation")

        record.save()

        return redirect("academic_records")

    return render(
        request,
        "edit_academic_record.html",
        {
            "record": record,
            "students": students
        }
    )


def delete_academic_record(request, record_id):

    if not request.user.is_authenticated:
        return redirect("login")

    record = AcademicRecord.objects.get(
        id=record_id
    )

    record.delete()

    return redirect("academic_records")


# =========================================================
# ML PERFORMANCE PREDICTION
# =========================================================

def predict_performance(request, record_id):

    if not request.user.is_authenticated:
        return redirect("login")

    record = AcademicRecord.objects.get(
        id=record_id
    )

    # Prepare input using the same feature names
    # used during model training

    input_data = pd.DataFrame([
        {
            "attendance": record.attendance,
            "internal_marks": record.internal_marks,
            "assignment_marks": record.assignment_marks,
            "previous_marks": record.previous_marks,
            "study_hours": record.study_hours,
            "backlogs": record.backlogs,
            "participation": record.participation
        }
    ])

    predicted_mark = model.predict(
        input_data
    )[0]

    predicted_mark = round(
        max(0, min(100, predicted_mark)),
        2
    )

    # -----------------------------------------------------
    # PERFORMANCE CATEGORY
    # -----------------------------------------------------

    if predicted_mark >= 80:

        performance = "Excellent"

    elif predicted_mark >= 60:

        performance = "Good"

    elif predicted_mark >= 50:

        performance = "Average"

    else:

        performance = "Poor"

    # -----------------------------------------------------
    # RISK LEVEL
    # -----------------------------------------------------

    if predicted_mark < 50:

        risk_level = "High"

    elif predicted_mark < 60:

        risk_level = "Medium"

    else:

        risk_level = "Low"

    # -----------------------------------------------------
    # SAVE PREDICTION
    # -----------------------------------------------------

    prediction = Prediction.objects.create(
        student=record.student,
        academic_record=record,
        predicted_mark=predicted_mark,
        performance=performance,
        risk_level=risk_level
    )

    return render(
        request,
        "prediction_result.html",
        {
            "prediction": prediction,
            "record": record
        }
    )


# =========================================================
# SUPPORT PLAN
# =========================================================

def add_support_plan(request, student_id):

    if not request.user.is_authenticated:
        return redirect("login")

    student = Student.objects.get(
        id=student_id
    )

    staff_members = Staff.objects.all()

    if request.method == "POST":

        support_type = request.POST.get("support_type")
        problem = request.POST.get("problem")
        action_taken = request.POST.get("action_taken")
        assigned_staff = request.POST.get("assigned_staff")
        status = request.POST.get("status")
        follow_up_date = request.POST.get("follow_up_date")
        remarks = request.POST.get("remarks")

        staff = None

        if assigned_staff:

            staff = Staff.objects.get(
                id=assigned_staff
            )

        SupportPlan.objects.create(
            student=student,
            support_type=support_type,
            problem=problem,
            action_taken=action_taken,
            assigned_staff=staff,
            status=status,
            follow_up_date=follow_up_date or None,
            remarks=remarks
        )

        return redirect("support_plans")

    return render(
        request,
        "add_support_plan.html",
        {
            "student": student,
            "staff_members": staff_members
        }
    )


def support_plans(request):

    if not request.user.is_authenticated:
        return redirect("login")

    plans = SupportPlan.objects.select_related(
        "student",
        "assigned_staff"
    ).order_by("-created_at")

    return render(
        request,
        "support_plans.html",
        {
            "plans": plans
        }
    )


def edit_support_plan(request, plan_id):

    if not request.user.is_authenticated:
        return redirect("login")

    plan = SupportPlan.objects.get(
        id=plan_id
    )

    staff_members = Staff.objects.all()

    if request.method == "POST":

        plan.support_type = request.POST.get(
            "support_type"
        )

        plan.problem = request.POST.get(
            "problem"
        )

        plan.action_taken = request.POST.get(
            "action_taken"
        )

        assigned_staff = request.POST.get(
            "assigned_staff"
        )

        if assigned_staff:

            plan.assigned_staff = Staff.objects.get(
                id=assigned_staff
            )

        else:

            plan.assigned_staff = None

        plan.status = request.POST.get(
            "status"
        )

        follow_up_date = request.POST.get(
            "follow_up_date"
        )

        if follow_up_date:

            plan.follow_up_date = follow_up_date

        else:

            plan.follow_up_date = None

        plan.remarks = request.POST.get(
            "remarks"
        )

        plan.save()

        return redirect("support_plans")

    return render(
        request,
        "edit_support_plan.html",
        {
            "plan": plan,
            "staff_members": staff_members
        }
    )


def delete_support_plan(request, plan_id):

    if not request.user.is_authenticated:
        return redirect("login")

    plan = SupportPlan.objects.get(
        id=plan_id
    )

    plan.delete()

    return redirect("support_plans")


# =========================================================
# HIGH RISK STUDENTS
# =========================================================

def high_risk_students(request):

    if not request.user.is_authenticated:
        return redirect("login")

    predictions = Prediction.objects.select_related(
        "student",
        "academic_record"
    ).filter(
        risk_level="High"
    ).order_by(
        "student_id",
        "-predicted_at"
    )

    # Same student-inte latest prediction mathram edukkuka
    latest_predictions = {}

    for prediction in predictions:
        if prediction.student_id not in latest_predictions:
            latest_predictions[prediction.student_id] = prediction

    predictions = latest_predictions.values()

    return render(
        request,
        "high_risk_students.html",
        {
            "predictions": predictions
        }
    )
# =========================================================
# PREDICTION HISTORY
# =========================================================

def prediction_history(request):

    if not request.user.is_authenticated:
        return redirect("login")

    predictions = Prediction.objects.select_related(
        "student",
        "academic_record"
    ).order_by("-predicted_at")

    return render(
        request,
        "prediction_history.html",
        {
            "predictions": predictions
        }
    )


# =========================================================
# STUDENT PERFORMANCE REPORT
# =========================================================

def student_report(request, student_id):

    if not request.user.is_authenticated:
        return redirect("login")

    student = Student.objects.get(
        id=student_id
    )

    academic_records = AcademicRecord.objects.filter(
        student=student
    ).order_by(
        "-semester",
        "-created_at"
    )

    predictions = Prediction.objects.filter(
        student=student
    ).order_by(
        "-predicted_at"
    )

    support_plans = SupportPlan.objects.filter(
        student=student
    ).order_by(
        "-created_at"
    )

    latest_prediction = predictions.first()

    context = {
        "student": student,
        "academic_records": academic_records,
        "predictions": predictions,
        "support_plans": support_plans,
        "latest_prediction": latest_prediction,
    }

    return render(
        request,
        "student_report.html",
        context
    )