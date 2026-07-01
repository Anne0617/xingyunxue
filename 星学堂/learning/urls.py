from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('employees', views.EmployeeViewSet)
router.register('programs', views.TrainingProgramViewSet)
router.register('nodes', views.CheckpointNodeViewSet)
router.register('employee-programs', views.EmployeeProgramViewSet)
router.register('employee-checkpoints', views.EmployeeCheckpointViewSet)

urlpatterns = [
    *router.urls,
    path('health/', views.api_health, name='api_health'),
    path('feedback/', views.api_feedback, name='api_feedback'),
    path('login/', views.api_login, name='api_login'),
    path('exams/', views.api_exams, name='api_exams'),
    path('exams/<slug:slug>/', views.api_exam_detail, name='api_exam_detail'),
    path('exams/<slug:slug>/submit/', views.api_exam_submit, name='api_exam_submit'),
    path('exams/<slug:slug>/results/', views.api_exam_results, name='api_exam_results'),
    path('exams/<slug:slug>/qrcode/', views.api_exam_qrcode, name='api_exam_qrcode'),
    path('badges/', views.api_badges, name='api_badges'),
    path('badges/claim/', views.api_claim_badge, name='api_claim_badge'),
    path('announcements/', views.api_announcements, name='api_announcements'),
    path('export/results/', views.api_export_results, name='api_export_results'),
    path('export/results/<slug:slug>/', views.api_export_results, name='api_export_results_slug'),
    path('daka/checkin/', views.daily_checkin, name='daily_checkin'),
    path('daka/leaderboard/', views.daka_leaderboard, name='daka_leaderboard'),
    path('daka/today/', views.daka_list_today, name='daka_list_today'),
    path('checkin/profile/', views.api_checkin_profile, name='api_checkin_profile'),
    path('checkin/progress/', views.api_checkin_progress, name='api_checkin_progress'),
    path('checkin/submit/', views.api_checkin_submit, name='api_checkin_submit'),
    path('checkin/leaderboard/', views.api_checkin_leaderboard, name='api_checkin_leaderboard'),
    path('checkin/admin/export/', views.api_checkin_export, name='api_checkin_export'),
    path('checkin/admin/overdue/', views.api_checkin_overdue, name='api_checkin_overdue'),
    path('checkin/qrcode/', views.api_checkin_qrcode, name='api_checkin_qrcode'),
    path('checkin/import/', views.api_checkin_import, name='api_checkin_import'),
    path('checkin/import-batch/', views.api_checkin_import_batch, name='api_checkin_import_batch'),
    path('checkin/admin-verify/', views.api_checkin_admin_verify, name='api_checkin_admin_verify'),
]

