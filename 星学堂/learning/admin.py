from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import *

admin.site.site_header = "星学堂 管理后台"
admin.site.site_title = "星学堂"
admin.site.index_title = "欢迎使用星学堂"

class QuestionInline(admin.TabularInline):
    model = Question; extra = 3

class ExamAdmin(admin.ModelAdmin):
    list_display = ("title","is_published","passing_score","max_attempts","start_time","end_time")
    list_filter = ("is_published","start_time")
    search_fields = ("title",); inlines = [QuestionInline]

class StudyAdmin(admin.ModelAdmin):
    list_display = ("name","company","department","position","wechat","submitted_at")
    list_filter = ("submitted_at","company")
    search_fields = ("name","company","description")

class ExamResultAdmin(admin.ModelAdmin):
    list_display = ("user_name","employee_id","company","department","exam","score","total_score","is_passed","submitted_at")
    list_filter = ("is_passed","submitted_at","exam")
    search_fields = ("user_name","employee_id")
    actions = ["export_csv"]
    
    def export_csv(self, request, queryset):
        import csv
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="exam_results.csv"'
        response.write(b"\ufeff")
        writer = csv.writer(response)
        writer.writerow(["姓名","工号","归属公司","部门","考试名称","得分","总分","是否及格","提交时间"])
        for r in queryset:
            writer.writerow([r.user_name, r.employee_id, r.company, r.department, r.exam.title, r.score, r.total_score, "是" if r.is_passed else "否", str(r.submitted_at)[:19]])
        return response
    export_csv.short_description = "导出选中记录为CSV"

class BadgeAdmin(admin.ModelAdmin): list_display = ("name","description","icon")
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ("user_name","badge","user_area","earned_at")
    list_filter = ("badge","earned_at")

class AnncAdmin(admin.ModelAdmin):
    list_display = ("title","date","is_published")
    list_filter = ("is_published","date")

class EmpAdmin(admin.ModelAdmin):
    list_display = ("employee_id","name","company","department","phone")
    search_fields = ("employee_id","name","company")

class ProgAdmin(admin.ModelAdmin): list_display = ("name","is_active","start_date","end_date")
class NodeAdmin(admin.ModelAdmin):
    list_display = ("name","program","node_type","order")
    list_filter = ("node_type","program")

class EmpProgAdmin(admin.ModelAdmin):
    list_display = ("employee","program","status")
    list_filter = ("status","program")

class EmpChkAdmin(admin.ModelAdmin):
    list_display = ("employee","node","status")
    list_filter = ("status",)

admin.site.register(Exam, ExamAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(UserBadge, UserBadgeAdmin)
admin.site.register(Announcement, AnncAdmin)
admin.site.register(Employee, EmpAdmin)
admin.site.register(TrainingProgram, ProgAdmin)
admin.site.register(CheckpointNode, NodeAdmin)
admin.site.register(EmployeeProgram, EmpProgAdmin)
admin.site.register(EmployeeCheckpoint, EmpChkAdmin)

@admin.register(CheckinContent)
class CheckinContentAdmin(admin.ModelAdmin):
    list_display = ("day_number", "title", "updated_at")
    list_editable = ("title",)
    ordering = ("day_number",)
    search_fields = ("title",)

@admin.register(CheckinMission)
class CheckinMissionAdmin(admin.ModelAdmin):
    list_display = ("day_number", "code", "name", "icon", "episode")
    list_editable = ("name", "icon", "episode")
    ordering = ("day_number",)
    search_fields = ("name", "code")


@admin.register(StarCheckinScore)
class StarCheckinScoreAdmin(admin.ModelAdmin):
    list_display = ("user_name", "day_number", "score", "hp_left", "is_passed", "completed_at")
    list_filter = ("day_number", "completed_at")
    search_fields = ("user__username", "user__first_name")
    date_hierarchy = "completed_at"
    actions = ["export_csv"]

    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_name.short_description = "用户"

    def is_passed(self, obj):
        return obj.score >= 4
    is_passed.short_description = "是否通关"
    is_passed.boolean = True

    def export_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
        response["Content-Disposition"] = "attachment; filename=star_checkin_scores.csv"
        response.write("\ufeff")
        w = csv.writer(response)
        w.writerow(["用户", "天数", "得分", "剩余生命", "是否通关", "完成时间"])
        for s in queryset:
            w.writerow([
                s.user.get_full_name() or s.user.username,
                s.day_number, s.score, s.hp_left,
                "是" if s.score >= 4 else "否",
                s.completed_at.strftime("%Y-%m-%d %H:%M"),
            ])
        return response
    export_csv.short_description = "导出选中记录为CSV"


@admin.register(StarDailyCheckin)
class StarDailyCheckinAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "checkin_date", "checkin_time", "ip_address")
    list_filter = ("checkin_date", "department")
    search_fields = ("name", "department")
    date_hierarchy = "checkin_date"
