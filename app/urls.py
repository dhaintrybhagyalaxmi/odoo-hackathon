from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('attendance/', views.attendance_view, name='attendance_view'),
    path('attendance/all/', views.attendance_admin_view, name='attendance_admin'),
    path('profile/', views.profile_view, name='profile_view'),
    path('leave/apply/', views.leave_apply_view, name='leave_apply'),
    path('leave/approval/', views.leave_approval_view, name='leave_approval'),
    path('employees/', views.employee_list_view, name='employee_list'),
    path('payroll/', views.payroll_view, name='payroll_view'),
]
