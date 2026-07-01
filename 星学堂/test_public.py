import urllib.request, json, re
base = "https://xingxuetang-production.up.railway.app"

# 测试提交
r = urllib.request.urlopen(base + "/api/checkin/submit/",
    data=json.dumps({"name":"测试员工","department":"品质管理部","day":2,"score":5,"hpLeft":4}).encode(),
    headers={"Content-Type":"application/json"})
print("提交:", r.status, json.loads(r.read())["message"])

# 排行榜
r2 = urllib.request.urlopen(base + "/api/checkin/leaderboard/")
data = json.loads(r2.read())
print("排行榜:", len(data), "人")
for u in data:
    print("  " + u["name"] + ": " + str(u["daysDone"]) + "关 " + str(u["totalScore"]) + "分")

# 管理员登录
from http.cookiejar import CookieJar
from urllib.parse import urlencode
cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
r3 = opener.open(base + "/admin/login/")
html = r3.read().decode()
m = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', html)
if m:
    token = m.group(1)
    d = urlencode({"username":"\u661f\u6cb3\u667a\u5584\u603b\u90e8","password":"xhzs2026","csrfmiddlewaretoken":token,"next":"/admin/learning/starcheckinscore/"})
    r4 = opener.open(base + "/admin/login/", data=d.encode())
    print("管理员登录:", r4.status)
    r5 = opener.open(base + "/admin/learning/starcheckinscore/")
    print("成绩页面:", r5.status)
else:
    print("CSRF token not found")
