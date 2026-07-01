import os

base = 'D:\\HuaweiMoveData\\Users\\Anna\\Documents\\星云学\\星学堂'

# Add URL routes
urls_file = os.path.join(base, 'learning', 'urls.py')
with open(urls_file, 'r+', encoding='utf-8') as f:
    c = f.read()
    if 'daily_checkin' not in c:
        c = c.replace("path('announcements/', views.api_announcements, name='api_announcements'),",
                      "path('announcements/', views.api_announcements, name='api_announcements'),\n" +
                      "    path('daka/checkin/', views.daily_checkin, name='daily_checkin'),\n" +
                      "    path('daka/leaderboard/', views.daka_leaderboard, name='daka_leaderboard'),\n" +
                      "    path('daka/today/', views.daka_list_today, name='daka_list_today'),")
        f.seek(0)
        f.write(c)
        f.truncate()
        print('URLs added')
    else:
        print('URLs already exist')

# Add admin registration
admin_file = os.path.join(base, 'learning', 'admin.py')
with open(admin_file, 'r+', encoding='utf-8') as f:
    c = f.read()
    if 'StarDailyCheckin' not in c:
        c = c.replace('from .models import', 'from .models import StarDailyCheckin,')
        c += '''

@admin.register(StarDailyCheckin)
class StarDailyCheckinAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "checkin_date", "checkin_time", "ip_address")
    list_filter = ("checkin_date", "department")
    search_fields = ("name", "department")
    date_hierarchy = "checkin_date"
'''
        f.seek(0)
        f.write(c)
        f.truncate()
        print('Admin registration added')
    else:
        print('Admin already registered')

print('Done')
