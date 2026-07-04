from django.contrib import admin
from .models import Profile, Attendance, LeaveRequest, Salary


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'role', 'department', 'designation', 'date_joined')
    list_filter = ('role', 'department')
    search_fields = ('employee_id', 'user__username', 'user__email')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'date')
    search_fields = ('employee__username',)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'applied_on')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__username',)


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'basic_salary', 'hra', 'bonus', 'deductions', 'net_salary')
    search_fields = ('employee__username',)