import os

fp = 'D:\\HuaweiMoveData\\Users\\Anna\\Documents\\星云学\\星学堂\\learning\\views.py'

with open(fp, 'r+', encoding='utf-8') as f:
    c = f.read()
    
    # Add import
    c = c.replace(
        'from .models import Study, Exam, Question, ExamResult, Badge, UserBadge, Announcement',
        'from .models import Study, Exam, Question, ExamResult, Badge, UserBadge, Announcement, StarDailyCheckin'
    )
    
    # Add view functions at the end
    c += r'''

@api_view(["POST"])
def daily_checkin(request):
    \"\"\"记录每日打卡\"\"\"
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
'''
    
    f.seek(0)
    f.write(c)
    f.truncate()
    print('Views added successfully')
    print(f'File size: {len(c)} chars')
