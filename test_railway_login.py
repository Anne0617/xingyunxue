import urllib.request, re
from http.cookiejar import CookieJar
from urllib.parse import urlencode

base = "https://xingxuetang-production.up.railway.app"
cj = CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

html = op.open(base + "/admin/login/").read().decode()
m = re.search(r'value="([^"]+)" name="csrfmiddlewaretoken"', html)
if not m:
    m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)

if m:
    for user, pwd in [("admin", "admin123"), ("星河智善总部", "xhzs2026")]:
        cj2 = CookieJar()
        op2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj2))
        h2 = op2.open(base + "/admin/login/").read().decode()
        t2 = re.search(r'value="([^"]+)" name="csrfmiddlewaretoken"', h2)
        if not t2:
            t2 = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', h2)
        if t2:
            d = urlencode({"username":user,"password":pwd,"csrfmiddlewaretoken":t2.group(1),"next":"/admin/learning/starcheckinscore/"}).encode()
            r = op2.open(base + "/admin/login/", data=d)
            try:
                r2 = op2.open(base + "/admin/learning/starcheckinscore/")
                print(f"{user}: LOGIN OK")
            except:
                print(f"{user}: FAILED (wrong credentials)")
else:
    print("Cannot find CSRF token")
