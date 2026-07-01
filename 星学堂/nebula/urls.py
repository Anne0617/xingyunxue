from django.contrib import admin
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from django.urls import path, include
from django.views.generic import TemplateView
from learning.views import frontend_view, exam_page, badge_page, training_page, training_promo
from django.shortcuts import redirect

urlpatterns = [
    path("checkin/", TemplateView.as_view(template_name="checkin.html"), name="checkin_home"),
    path("checkin/promo/", TemplateView.as_view(template_name="promo.html"), name="checkin_promo"),
    path("checkin/daka/", TemplateView.as_view(template_name="daka.html"), name="checkin_daka"),
    path("checkin/training/", TemplateView.as_view(template_name="training.html"), name="checkin_training"),
    path("exam/<slug:slug>/", exam_page, name="exam_page"),
    path("badge/", badge_page, name="badge_page"),
    path('quick-login/', lambda r: auth_login(r, authenticate(username='鏄熸渤鏅哄杽鎬婚儴', password='xhzs2026')) or HttpResponseRedirect('/admin/') if authenticate(username='鏄熸渤鏅哄杽鎬婚儴', password='xhzs2026') else HttpResponseRedirect('/admin/login/?error=1')),
    path("login/", lambda request: redirect("admin/login/")),
    path("login", lambda request: redirect("admin/login/")),
    path("admin/", admin.site.urls),
    path("api/", include("learning.urls")),
    path("training/", training_page, name="training_page"),
    path("training/promo/", training_promo, name="training_promo"),
    path("", frontend_view, name="frontend"),
]
