
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.views.generic import TemplateView
from .serializers import StudySerializer, ExamSerializer, ExamResultSerializer, BadgeSerializer, UserBadgeSerializer
from .models import Study, Exam, Question, ExamResult, Badge, UserBadge, Announcement, StarDailyCheckin, StarCheckinScore
from django.db.models import Count, Sum
import csv
from io import StringIO

@api_view(["GET"])
def api_health(request):
    return Response({"status":"ok","message":"星学堂 API 运行正常","version":"1.0.0"})

@api_view(["POST"])
@csrf_exempt
def api_login(request):
    username = request.data.get("username","")
    password = request.data.get("password","")
    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
        return Response({"success":True,"redirect":"/admin/"})
    return Response({"success":False,"message":"用户名或密码错误"}, status=400)

@api_view(["POST"])
@csrf_exempt
def api_feedback(request):
    serializer = StudySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"提交成功","data":serializer.data}, status=201)
    return Response({"message":"提交失败","errors":serializer.errors}, status=400)

@api_view(["GET"])
def api_exams(request):
    exams = Exam.objects.filter(is_published=True) if not request.GET.get("all") else Exam.objects.all()
    data = []
    for e in exams:
        data.append({"title":e.title,"description":e.description,"slug":str(e.slug),"passing_score":e.passing_score})
    return Response(data)

@api_view(["GET"])
def api_exam_detail(request, slug):
    exam = Exam.objects.filter(slug=slug).first()
    if not exam: return Response({"error":"考试不存在"}, status=404)
    questions = Question.objects.filter(exam=exam).order_by("sort_order")
    qlist = []
    for q in questions:
        qlist.append({"id":q.id,"content":q.content,"type":q.question_type,"options":{"A":q.option_a,"B":q.option_b,"C":q.option_c,"D":q.option_d},"score":q.score})
    return Response({"exam":{"title":exam.title,"description":exam.description},"questions":qlist})

@api_view(["POST"])
@csrf_exempt
def api_exam_submit(request, slug):
    exam = Exam.objects.filter(slug=slug).first()
    if not exam: return Response({"error":"考试不存在"}, status=404)
    user_name = request.data.get("user_name","")
    user_area = request.data.get("user_area","")
    employee_id = request.data.get("employee_id","")
    phone = request.data.get("phone","")
    company = request.data.get("company","")
    department = request.data.get("department","")
    answers = request.data.get("answers",{})
    questions = Question.objects.filter(exam=exam)
    total = sum(q.score for q in questions)
    score = 0
    for q in questions:
        if answers.get(str(q.id),"") == q.answer: score += q.score
    passed = score >= exam.passing_score
    attempt = ExamResult.objects.filter(exam=exam, user_name=user_name).count() + 1
    ExamResult.objects.create(exam=exam, user_name=user_name, user_area=user_area,
        employee_id=employee_id, phone=phone, company=company, department=department,
        score=score, total_score=total, is_passed=passed, attempt_num=attempt)
    return Response({"score":score,"total":total,"passed":passed,"attempt":attempt})

@api_view(["GET"])
def api_exam_results(request, slug):
    exam = Exam.objects.filter(slug=slug).first()
    if not exam: return Response({"error":"考试不存在"}, status=404)
    results = ExamResult.objects.filter(exam=exam).order_by("-submitted_at")
    data = []
    for r in results:
        data.append({"user":r.user_name,"score":r.score,"total":r.total_score,"passed":r.is_passed,"date":str(r.submitted_at)})
    return Response(data)

@api_view(["GET"])
def api_exam_qrcode(request, slug):
    from django.http import JsonResponse
    return JsonResponse({"url":request.build_absolute_uri("/exam/"+slug+"/")})

@api_view(["GET"])
def api_badges(request):
    data = []
    for b in Badge.objects.all():
        data.append({"name":b.name,"description":b.description,"icon":b.icon})
    return Response(data)

@api_view(["POST"])
@csrf_exempt
def api_claim_badge(request):
    badge_id = request.data.get("badge_id")
    user_name = request.data.get("user_name","")
    badge = Badge.objects.filter(id=badge_id).first()
    if not badge: return Response({"error":"称号不存在"}, status=404)
    ub, created = UserBadge.objects.get_or_create(badge=badge, user_name=user_name)
    return Response({"success":True,"newly_claimed":created})

def exam_page(request, slug):
    exam = Exam.objects.filter(slug=slug).first()
    if not exam: return HttpResponse("考试不存在")
    questions = Question.objects.filter(exam=exam).order_by("sort_order")
    return render(request, "learning/exam.html", {"exam":exam,"questions":questions,"slug":slug})

def badge_page(request):
    return render(request, "learning/badge.html", {"badges":Badge.objects.all()})

def challenge_page(request):
    exam = Exam.objects.filter(is_published=True).first()
    questions = Question.objects.filter(exam=exam).order_by("sort_order")[:3] if exam else []
    return render(request, "learning/challenge.html", {"exam":exam,"questions":questions})

@api_view(["GET"])
def api_announcements(request):
    qs = Announcement.objects.filter(is_published=True).order_by("-date")[:10]
    data = []
    for a in qs:
        data.append({"date":a.date.strftime("%Y-%m-%d"),"title":a.title})
    return Response(data)

def api_download(request, filename):
    import os, mimetypes
    mimetypes.add_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx")
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist", "downloads")
    filepath = os.path.join(base, filename)
    if not os.path.exists(filepath):
        raise Http404("文件不存在")
    response = FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)
    response["Content-Type"] = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    return response

@api_view(["GET"])
def api_export_results(request, slug=None):
    """导出考试成绩为CSV"""
    from django.http import HttpResponse
    import csv
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="exam_results.csv"'
    response.write(b"\ufeff")
    writer = csv.writer(response)
    writer.writerow(["姓名","工号","归属公司","部门","考试","得分","总分","是否及格","提交时间"])
    
    if slug:
        results = ExamResult.objects.filter(exam__slug=slug)
    else:
        results = ExamResult.objects.all()
    
    for r in results.order_by("-submitted_at"):
        writer.writerow([r.user_name, r.employee_id, r.company, r.department, 
                        r.exam.title, r.score, r.total_score, 
                        "是" if r.is_passed else "否", str(r.submitted_at)[:19]])
    return response


def training_page(request):
    from django.http import HttpResponse
    import os
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fp = os.path.join(base, '新星启航培训.html')
    with open(fp, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read())

def training_promo(request):
    from django.http import HttpResponse
    import os
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fp = os.path.join(base, 'star_course', '培训宣传页.html')
    with open(fp, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read())
frontend_view = lambda request: redirect('checkin_home')


# === 闯关系统 ViewSets ===
from rest_framework import viewsets, filters
from .models import Employee, TrainingProgram, CheckpointNode, EmployeeProgram, EmployeeCheckpoint
from .serializers import (EmployeeSerializer, TrainingProgramSerializer, CheckpointNodeSerializer,
    EmployeeProgramSerializer, EmployeeCheckpointSerializer)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["employee_id", "name"]

class TrainingProgramViewSet(viewsets.ModelViewSet):
    queryset = TrainingProgram.objects.filter(is_active=True)
    serializer_class = TrainingProgramSerializer

class CheckpointNodeViewSet(viewsets.ModelViewSet):
    queryset = CheckpointNode.objects.all()
    serializer_class = CheckpointNodeSerializer
    filterset_fields = ["program"]

class EmployeeProgramViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProgram.objects.all()
    serializer_class = EmployeeProgramSerializer
    filterset_fields = ["program", "employee"]

class EmployeeCheckpointViewSet(viewsets.ModelViewSet):
    queryset = EmployeeCheckpoint.objects.all()
    serializer_class = EmployeeCheckpointSerializer
    filterset_fields = ["employee", "node", "status"]

    def perform_update(self, serializer):
        instance = self.get_object()
        old = instance.status
        serializer.save()
        if old != "completed" and serializer.validated_data.get("status") == "completed":
            next_node = CheckpointNode.objects.filter(
                program=instance.node.program, order__gt=instance.node.order
            ).order_by("order").first()
            if next_node:
                EmployeeCheckpoint.objects.update_or_create(
                    employee=instance.employee, node=next_node, defaults={"status": "current"}
                )


@api_view(["POST"])
def daily_checkin(request):
    """记录每日打卡"""
    from datetime import date
    name = request.data.get("name", "").strip()
    dept = request.data.get("department", "").strip()
    phone = request.data.get("phone", "").strip()
    if not name:
        return Response({"error": "请填写姓名"}, 400)
    today = date.today()
    existing = StarDailyCheckin.objects.filter(name=name, checkin_date=today).first()
    if existing:
        return Response({"success": True, "message": "今日已打卡", "first": False})
    StarDailyCheckin.objects.create(
        name=name, department=dept, phone=phone,
        checkin_date=today,
        ip_address=request.META.get("REMOTE_ADDR", "")
    )
    return Response({"success": True, "message": "打卡成功", "first": True})

@api_view(["GET"])
def daka_leaderboard(request):
    from django.db.models import Count
    data = StarDailyCheckin.objects.values("name", "department").annotate(
        days=Count("checkin_date", distinct=True)
    ).order_by("-days")[:50]
    return Response([
        {"rank": i+1, "name": r["name"], "department": r["department"], "days": r["days"]}
        for i, r in enumerate(data)
    ])

@api_view(["GET"])
def daka_list_today(request):
    from datetime import date
    today = date.today()
    qs = StarDailyCheckin.objects.filter(checkin_date=today).values("name", "department", "checkin_time")
    return Response(list(qs))


# ====== 十五五闯关 API ======

@api_view(["GET"])
def api_checkin_profile(request):
    name = request.GET.get("name", "")
    if not name:
        return Response({"error": "缺少 name 参数"}, status=400)
    return Response({
        "name": name,
        "department": request.GET.get("department", ""),
        "phone": request.GET.get("phone", ""),
    })

@api_view(["GET"])
def api_checkin_progress(request):
    name = request.GET.get("name", "")
    if not name:
        return Response({"error": "缺少 name 参数"}, status=400)
    rows = StarCheckinScore.objects.filter(
        user__username=name
    ).values("day_number", "score", "hp_left", "answers_json", "completed_at")
    days = {}
    for r in rows:
        day = r["day_number"]
        days[f"d{day}"] = {
            "score": r["score"],
            "hpLeft": r["hp_left"],
            "answered": json.loads(r["answers_json"]) if r["answers_json"] else {},
            "date": r["completed_at"].strftime("%Y-%m-%d %H:%M") if r["completed_at"] else "",
        }
    return Response({"days": days})

@api_view(["POST"])
@csrf_exempt
def api_checkin_submit(request):
    data = request.data
    name = data.get("name", "")
    department = data.get("department", "")
    phone = data.get("phone", "")
    day = data.get("day")
    score = data.get("score")
    hp_left = data.get("hpLeft", 5)
    answers = data.get("answers", {})

    if not name or not day or score is None:
        return Response({"error": "参数不完整"}, status=400)

    # 获取或创建用户（简化：用 username 标识）
    from django.contrib.auth.models import User
    user, _ = User.objects.get_or_create(
        username=name,
        defaults={"first_name": name}
    )
    # 更新用户信息
    if department and not user.last_name:
        user.last_name = department
    if phone and not user.email:
        user.email = phone
    user.save()

    # 检查是否已提交该关
    existing = StarCheckinScore.objects.filter(user=user, day_number=day).first()
    if existing:
        return Response({"error": "该关已提交，不可重复提交"}, status=409)

    StarCheckinScore.objects.create(
        user=user,
        day_number=day,
        score=score,
        hp_left=hp_left,
        answers_json=json.dumps(answers, ensure_ascii=False),
    )
    return Response({"success": True, "message": "提交成功"})

@api_view(["GET"])
def api_checkin_leaderboard(request):
    from django.db.models import Count, Sum
    # Individual rankings with department
    data = StarCheckinScore.objects.values("user__username", "user__last_name").annotate(
        days_done=Count("day_number", distinct=True),
        total_score=Sum("score"),
    ).order_by("-total_score", "-days_done")[:50]

    individual = []
    for i, r in enumerate(data):
        individual.append({
            "rank": i + 1,
            "name": r["user__username"],
            "department": r["user__last_name"] or "",
            "daysDone": r["days_done"],
            "totalScore": r["total_score"],
        })

    # Department rankings
    dept = StarCheckinScore.objects.values("user__last_name").annotate(
        total_score=Sum("score"),
        total_days=Count("day_number"),
        user_count=Count("user", distinct=True),
    ).order_by("-total_score")

    dept_ranking = []
    for i, r in enumerate(dept):
        dept_ranking.append({
            "rank": i + 1,
            "department": r["user__last_name"] or "未填写",
            "totalScore": r["total_score"],
            "totalDays": r["total_days"],
            "userCount": r["user_count"],
        })

    return Response({"individual": individual, "department": dept_ranking})

@api_view(["GET"])
def api_checkin_export(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response({"error": "无权限"}, status=403)
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = "attachment; filename=star_course_export.csv"
    response.write("\ufeff")  # BOM for Excel

    writer = csv.writer(response)
    headers = ["姓名", "部门", "联系方式", "总积分", "通关数"]
    for d in range(1, 31):
        headers.append(f"第{d}关")
    writer.writerow(headers)

    users = StarCheckinScore.objects.values_list(
        "user__username", "user__last_name", "user__email"
    ).distinct()
    for u in users:
        username, dept, phone = u
        scores = StarCheckinScore.objects.filter(user__username=username).values_list("day_number", "score")
        score_dict = {s[0]: s[1] for s in scores}
        total = sum(score_dict.values())
        row = [username, dept or "", phone or "", total, len(score_dict)]
        for d in range(1, 31):
            row.append(score_dict.get(d, ""))
        writer.writerow(row)
    return response

@api_view(["GET"])
def api_checkin_overdue(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response({"error": "无权限"}, status=403)
    deadline_day = int(request.GET.get("deadlineDay", 5))
    all_users = set(
        StarCheckinScore.objects.values_list("user__username", flat=True).distinct()
    )
    overdue_users = []
    for uname in all_users:
        cnt = StarCheckinScore.objects.filter(user__username=uname, day_number__lte=deadline_day).count()
        if cnt == 0:
            user_obj = StarCheckinScore.objects.filter(user__username=uname).first()
            overdue_users.append({
                "name": uname,
                "department": user_obj.user.last_name if user_obj else "",
                "phone": user_obj.user.email if user_obj else "",
            })
    return Response({"deadlineDay": deadline_day, "count": len(overdue_users), "users": overdue_users})

@api_view(["POST"])
@csrf_exempt
def api_checkin_import(request):
    """从旧 GitHub Pages 站点导入（localStorage 数据）"""
    data = request.data
    if not data:
        return Response({"error": "请提供数据"}, status=400)

    imported = 0
    # 格式: [{name, dept, phone, days: {d1: {score,hpLeft,answered}, ...}}]
    users = data if isinstance(data, list) else data.get("users", [data])

    from django.contrib.auth.models import User
    results = []

    for u in users:
        name = u.get("name", "")
        dept = u.get("dept", "")
        phone = u.get("phone", "")
        days = u.get("days", u.get("scores", {}))
        if not name or not days:
            continue

        # 创建用户
        user, _ = User.objects.get_or_create(username=name, defaults={"first_name": name})
        if dept: user.last_name = dept
        if phone: user.email = phone
        user.save()

        for day_key, day_data in days.items():
            day_num = int(day_key.replace("d", ""))
            score = day_data.get("score", 0) if isinstance(day_data, dict) else day_data
            hp_left = day_data.get("hpLeft", 5) if isinstance(day_data, dict) else 5
            answers = day_data.get("answered", {}) if isinstance(day_data, dict) else {}

            existing = StarCheckinScore.objects.filter(user=user, day_number=day_num).first()
            if not existing:
                StarCheckinScore.objects.create(
                    user=user, day_number=day_num,
                    score=score, hp_left=hp_left,
                    answers_json=json.dumps(answers, ensure_ascii=False),
                )
                imported += 1

        results.append({"name": name, "days": len(days), "imported": imported})

    return Response({"message": f"成功导入 {imported} 条记录", "users": results})

@api_view(["POST"])
@csrf_exempt
def api_checkin_import_batch(request):
    """批量导入多用户数据"""
    rows = request.data
    if not isinstance(rows, list):
        return Response({"error": "请提供数组格式的数据"}, status=400)

    from django.contrib.auth.models import User
    imported = 0
    errors = []

    for row in rows:
        name = row.get("name", "")
        day = row.get("day")
        score = row.get("score", 0)
        hp = row.get("hp", 5)
        if not name or not day:
            errors.append({"row": row, "error": "缺少 name 或 day"})
            continue
        user, _ = User.objects.get_or_create(username=name, defaults={"first_name": name})
        existing = StarCheckinScore.objects.filter(user=user, day_number=day).first()
        if not existing:
            StarCheckinScore.objects.create(
                user=user, day_number=day, score=score, hp_left=hp
            )
            imported += 1

    return Response({"imported": imported, "errors": errors})

@api_view(["GET"])
def api_checkin_qrcode(request):
    """生成闯关页面二维码"""
    try:
        import qrcode, io
        url = request.build_absolute_uri("/checkin/")
        img = qrcode.make(url)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return HttpResponse(buf.getvalue(), content_type="image/png")
    except ImportError:
        return Response({"error": "需要安装 qrcode 库"}, status=500)


@api_view(["POST"])
@csrf_exempt
def api_checkin_admin_verify(request):
    """验证管理员密码（闯关页面内嵌管理面板用）"""
    from django.conf import settings
    pwd = request.data.get("password", "")
    expected = getattr(settings, "ADMIN_PANEL_PASSWORD", "admin123")
    if pwd == expected:
        return Response({"valid": True})
    return Response({"valid": False}, status=403)
