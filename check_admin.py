import urllib.request, re
from http.cookiejar import CookieJar
from urllib.parse import urlencode

base = "https://xingxuetang-production.up.railway.app"
cj = CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

html = op.open(base + "/admin/login/").read().decode()
m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
if not m:
    m = re.search(r'value="([^"]+)" name="csrfmiddlewaretoken"', html)
if m:
    t = m.group(1)
    d = urlencode({"username":"admin","password":"admin123","csrfmiddlewaretoken":t,"next":"/admin/"}).encode()
    r = op.open(base + "/admin/login/", data=d)
    r2 = op.open(base + "/admin/")
    h2 = r2.read().decode()
    # 提取所有模型链接
    links = re.findall(r'href="([^"]+)"[^>]*>([^<]+)</a>', h2)
    for href, name in links:
        if "learning" in href:
            print(name.strip(), "->", href)
else:
    print("CSRF error")
