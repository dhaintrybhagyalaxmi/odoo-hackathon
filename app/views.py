from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import SignUpForm, ProfileEditForm, LeaveRequestForm
from .models import Profile, Attendance, LeaveRequest, Salary


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role == 'admin':
        return render(request, 'admin_dashboard.html', {'profile': profile})
    else:
        return render(request, 'employee_dashboard.html', {'profile': profile})


@login_required
def attendance_view(request):
    today = timezone.now().date()
    attendance, created = Attendance.objects.get_or_create(
        employee=request.user,
        date=today
    )

    if request.method == 'POST':
        action = request.POST.get('action')
        now = timezone.now().time()
        if action == 'check_in' and not attendance.check_in:
            attendance.check_in = now
            attendance.status = 'present'
            attendance.save()
        elif action == 'check_out' and attendance.check_in and not attendance.check_out:
            attendance.check_out = now
            attendance.save()
        return redirect('attendance_view')

    records = Attendance.objects.filter(employee=request.user).order_by('-date')[:30]
    return render(request, 'attendance.html', {
        'today_record': attendance,
        'records': records
    })


@login_required
def attendance_admin_view(request):
    records = Attendance.objects.all().order_by('-date')[:100]
    return render(request, 'attendance_admin.html', {'records': records})


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_view')
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'profile.html', {'profile': profile, 'form': form})


@login_required
def leave_apply_view(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, 'Leave request submitted.')
            return redirect('leave_apply')
    else:
        form = LeaveRequestForm()

    my_leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-applied_on')
    return render(request, 'leave_apply.html', {'form': form, 'my_leaves': my_leaves})


@login_required
def leave_approval_view(request):
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')
        comment = request.POST.get('admin_comment', '')
        leave = LeaveRequest.objects.get(id=leave_id)
        if action == 'approve':
            leave.status = 'approved'
        elif action == 'reject':
            leave.status = 'rejected'
        leave.admin_comment = comment
        leave.save()
        return redirect('leave_approval')

    leaves = LeaveRequest.objects.all().order_by('-applied_on')
    return render(request, 'leave_approval.html', {'leaves': leaves})


@login_required
def employee_list_view(request):
    profiles = Profile.objects.select_related('user').all()
    return render(request, 'employee_list.html', {'profiles': profiles})


@login_required
def payroll_view(request):
    profile = Profile.objects.get(user=request.user)
    salary, created = Salary.objects.get_or_create(employee=request.user)

    if profile.role == 'admin' and request.method == 'POST':
        emp_id = request.POST.get('employee_id')
        salary_obj = Salary.objects.get(employee_id=emp_id)
        salary_obj.basic_salary = request.POST.get('basic_salary') or 0
        salary_obj.hra = request.POST.get('hra') or 0
        salary_obj.bonus = request.POST.get('bonus') or 0
        salary_obj.deductions = request.POST.get('deductions') or 0
        salary_obj.save()
        return redirect('payroll_view')

    if profile.role == 'admin':
        all_salaries = []
        for p in Profile.objects.select_related('user').all():
            s, _ = Salary.objects.get_or_create(employee=p.user)
            all_salaries.append(s)
        return render(request, 'payroll_admin.html', {'salaries': all_salaries})
    else:
        return render(request, 'payroll.html', {'salary': salary})
