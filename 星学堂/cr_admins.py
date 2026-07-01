import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebula.settings')
django.setup()
from django.contrib.auth.models import User

admins = [
    ('admin', 'admin@test.com', 'admin123'),
    ('星河智善总部', 'admin@xingxuetang.com', 'xhzs2026'),
]

for uname, email, pwd in admins:
    u, created = User.objects.get_or_create(username=uname, defaults={'is_superuser':True,'is_staff':True})
    u.set_password(pwd)
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print(f'OK: {uname} / {pwd}')
